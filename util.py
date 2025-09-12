import nltk
from nltk.stem import PorterStemmer
from typing import Dict, List, Set

def resolve_entity_conflicts(
    node_values_entries: Dict,
    node_property_entries: Dict, 
    node_label_entries: Dict,
    language: str = 'en',
    remove_common_words: bool = True
) -> Dict:
    """
    Remove node_values that conflict with node_properties and node_labels
    after stemming/lemmatization, and optionally filter out common words.
    
    Args:
        node_values_entries: Dictionary of node values
        node_property_entries: Dictionary of node properties  
        node_label_entries: Dictionary of node labels
        language: Language for stemming (default: 'en')
        remove_common_words: Whether to remove common English words
        
    Returns:
        Filtered node_values_entries dictionary
    """
    
    # Initialize stemmer
    stemmer = PorterStemmer()
    
    # Common words that often cause false matches
    COMMON_WORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'been', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to',
        'was', 'will', 'with', 'have', 'had', 'do', 'did', 'can', 'could',
        'would', 'should', 'may', 'might', 'must', 'shall', 'this', 'these',
        'those', 'they', 'them', 'their', 'what', 'when', 'where', 'who',
        'why', 'how', 'which', 'act', 'acted', 'acting'  # Add problematic verbs
    }
    
    def stem_text(text: str) -> str:
        """Stem a text string"""
        if not text or text.isupper():  # Skip empty or all-caps words
            return text
        return stemmer.stem(text.lower())
    
    # Step 1: Create sets of stemmed properties and labels
    stemmed_properties: Set[str] = set()
    stemmed_labels: Set[str] = set()
    
    print("Building stemmed properties and labels...")
    
    # Add stemmed property entries
    for prop_key in node_property_entries:
        stemmed_prop = stem_text(prop_key)
        if stemmed_prop:
            stemmed_properties.add(stemmed_prop)
        
        # Add synonyms
        for synonym in node_property_entries[prop_key]:
            stemmed_synonym = stem_text(synonym)
            if stemmed_synonym:
                stemmed_properties.add(stemmed_synonym)
    
    # Add stemmed label entries  
    for label_key in node_label_entries:
        stemmed_label = stem_text(label_key)
        if stemmed_label:
            stemmed_labels.add(stemmed_label)
            
        # Add synonyms
        for synonym in node_label_entries[label_key]:
            stemmed_synonym = stem_text(synonym)
            if stemmed_synonym:
                stemmed_labels.add(stemmed_synonym)
    
    print(f"Found {len(stemmed_properties)} unique stemmed properties")
    print(f"Found {len(stemmed_labels)} unique stemmed labels")
    
    # Step 2: Filter node_values_entries
    filtered_values = {}
    removed_conflicts = []
    removed_common = []
    
    print("Filtering node values...")
    
    for value_key in node_values_entries:
        stemmed_value = stem_text(value_key)
        should_keep = True
        removal_reason = None
        
        # Check if stemmed value conflicts with properties
        if stemmed_value in stemmed_properties:
            should_keep = False
            removal_reason = f"conflicts with property (stemmed: '{stemmed_value}')"
            
        # Check if stemmed value conflicts with labels
        elif stemmed_value in stemmed_labels:
            should_keep = False
            removal_reason = f"conflicts with label (stemmed: '{stemmed_value}')"
            
        # Check if it's a common word
        elif remove_common_words and stemmed_value in COMMON_WORDS:
            should_keep = False
            removal_reason = f"common word (stemmed: '{stemmed_value}')"
        
        # Check if it's too short (likely not meaningful)
        elif len(stemmed_value) <= 2:
            should_keep = False  
            removal_reason = f"too short (stemmed: '{stemmed_value}')"
        
        if should_keep:
            filtered_values[value_key] = node_values_entries[value_key]
        else:
            if "conflicts with" in removal_reason:
                removed_conflicts.append((value_key, removal_reason))
            else:
                removed_common.append((value_key, removal_reason))
    
    # Print summary
    print(f"\nFiltering Summary:")
    print(f"Original values: {len(node_values_entries)}")
    print(f"Filtered values: {len(filtered_values)}")
    print(f"Removed conflicts: {len(removed_conflicts)}")
    print(f"Removed common/short: {len(removed_common)}")
    
    if removed_conflicts:
        print(f"\nRemoved conflicts (showing first 10):")
        for value, reason in removed_conflicts[:10]:
            print(f"  '{value}' - {reason}")
        if len(removed_conflicts) > 10:
            print(f"  ... and {len(removed_conflicts) - 10} more")
    
    if removed_common:
        print(f"\nRemoved common/short words (showing first 10):")
        for value, reason in removed_common[:10]:
            print(f"  '{value}' - {reason}")
        if len(removed_common) > 10:
            print(f"  ... and {len(removed_common) - 10} more")
    
    return filtered_values

# Usage example:
# filtered_node_values = resolve_entity_conflicts(
#     node_values_entries,
#     node_property_entries, 
#     node_label_entries,
#     language='en',
#     remove_common_words=True
# )
# 
# # Update your node_values_entries
# node_values_entries = filtered_node_values