export default {
  header: {
    home: 'Home',
    search: 'Search',
    about: 'About',
    language: 'Language'
  },
  home: {
    welcome: 'Welcome to Struct2SL',
    subtitle: 'Discover synthetic lethality pairs and gain deeper insights into genetic interactions.',
    searchPlaceholder: 'Search gene pairs...(e.g.: TSPAN1)',
    stats: {
      genePairs: 'Gene Pairs',
      experiments: 'Experiments',
      cancerTypes: 'Cancer Types',
      publications: 'Publications'
    },
    updates: {
      title: 'Recent Updates',
      newBreastCancer: {
        title: 'New Breast Cancer Gene Pairs',
        content: 'We have added 342 new synthetic lethality gene pairs related to breast cancer, providing new potential targets for breast cancer treatment.',
        date: 'Updated on 2025-06-15'
      },
      websiteOptimization: {
        title: 'Website Interface Optimization',
        content: 'We have optimized the website interface, improving user experience and search functionality for more convenient data retrieval.',
        date: 'Updated on 2025-06-01'
      }
    },
    statistics: {
      title: 'Statistics of Struct2SL',
      description: 'Struct2SL uses the latest research data from SynLethDB (human synthetic lethal gene pairs and non-synthetic lethal gene pairs) to predict potential gene pairs. The current version covers 15794 human genes, and the results presented are computational prediction results.',
      table: {
        header: {
          dataType: 'Types of data',
          entityCount: 'Number of entities'
        },
        rows: {
          syntheticLethalPairs: 'Synthetic lethal gene pairs',
          nonsyntheticLethalPairs: 'Nonsynthetic lethal gene pairs',
          proteinSequence: 'Protein sequence',
          ppiNodesCount: 'Protein-Protein Interaction Networks (nodes)',
          ppiEdgesCount: 'Protein-Protein Interaction Networks (edges)',
          proteinStructure: 'Protein spatial structure'
        }
      }
    }
  },
  search: {
    title: 'Search Gene Pairs',
    gene1: 'Gene 1',
    gene2: 'Gene 2 (Optional)',
    inputPlaceholder: 'Enter gene name',
    searchButton: 'Search',
    results: 'Search Results',
    table: {
      gene1: 'Gene 1',
      gene2: 'Gene 2',
      predictionScore: 'Prediction Score',
      predictingRelation: 'Predicting Relation',
      source: 'Source'
    },
    pagination: {
      showing: 'Showing',
      to: 'to',
      of: 'of',
      results: 'results',
      previous: 'Previous',
      next: 'Next',
      goToPage: 'go to page',
      Page: '',
      go: 'Go ',
    },
    noResults: {
      title: 'No Matching Results Found',
      suggestion: 'Try using different search criteria or keywords',
      reset: 'Reset Search'
    },
    loading: 'Searching...'
  },
  about: {
    title: 'About Struct2SL',
    description: 'Struct2SL is a database focused on synthetic lethality gene pairs, providing potential targets for cancer treatment. For\
            more detailed instructions, please refer to',
    link: 'here',
    sections: {
      whatIs: {
        title: 'What is Synthetic Lethality?',
        content: 'Synthetic lethality refers to a relationship between two genes where knocking out either gene alone allows cell survival, but simultaneously knocking out both genes leads to cell death. This concept is significant in cancer treatment as it can help identify specific therapeutic targets for cancer cells.'
      },
      ourMission: {
        title: 'Our Mission',
        content: 'We are committed to predicting and validating synthetic lethality gene pairs by integrating multiple data sources and advanced computational methods, providing scientific basis for precision cancer treatment.'
      },
      contact: {
        title: 'Contact Us',
        email: 'Email',
        phone: 'Phone'
      }
    }
  },
  footer: {
    about: {
      title: 'About Struct2SL',
      description: 'Struct2SL is a database focused on synthetic lethality gene pairs, providing potential targets for cancer treatment.'
    },
    quickLinks: {
      title: 'Quick Links',
      home: 'Home',
      search: 'Search',
      about: 'About'
    },
    resources: {
      title: 'Resources',
      apiDocs: 'API Documentation',
      tutorials: 'Tutorials',
      download: 'Download Data',
      faq: 'FAQ'
    },
    contact: {
      title: 'Contact Us'
    },
    copyright: 'All rights reserved.'
  }
}