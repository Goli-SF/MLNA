# Table of Contents

<!-- TOC -->

- [Project Title](#project-title)
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Words of thanks](#words-of-thanks)

<!-- /TOC -->

# Project Title
The MultiLingual Network Analysis Package (mlna)

Developed by [Golnaz Sarkar Farshi](https://orcid.org/0000-0002-8870-0954)

Version 0.1.0 (semantic versioning)

# Description
*This project was funded in 2024 by the [Flex Funds of NFDI4Culture](https://nfdi4culture.de/de/dienste/details/flex-funds.html), a member consortium of the National Research Data Infrastructure in Germany.*

*NFDI4Culture is funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) under the National Research Data Infrastructure – Project Number: 441958017.*

**If you use MLNA in your scientific project, please cite [this article](https://www.sciencedirect.com/science/article/pii/S2352711025000718).**


MLNA is designed for researchers in the humanities who wish to work with multilingual digital documents, even if they do not fully understand the languages in which these documents are written. The tool helps researchers identify and select relevant documents from large digital collections for their research topics. The primary aim of this package is to integrate digital historical texts in non-European languages into European research, and vice versa.

To achieve this, the package enables users to visualize network relationships between words and entities extracted from the texts. These network visualizations reveal connections between specific keywords (e.g., people, places, technologies, dates, products, events, etc) mentioned in the documents. By examining these relationships, users can filter texts that discuss a specific connection (an edge in the network graph) or include a particular word (a node in the network graph) for closer reading and detailed analysis.

Beyond its primary use case in research, the package can also be employed for general network visualization or basic text data cleaning.

In addition to reading the following content, you can watch this [video tutorial](https://youtu.be/FuPgneZ5wGU) on YouTube to learn how to use **mlna** in Python. If you'd like to follow along with the video tutorial, you can access the data and Jupyter Notebook provided in the [material4tutorial](https://github.com/Goli-SF/MLNA/tree/main/material4tutorial) folder.

If you are not familiar with Python and prefer to use the package with a user-friendly interface, you can watch the [video tutorial](https://youtu.be/3c1C4b4D9BI) for the **mlna-app** on YouTube.

# Installation
Before installing mlna, make sure to create a virtual environment in your working directory to avoid dependency conflicts. If you plan to use Jupyter Notebook or Jupyter Lab, install them within your virtual environment first, before installing mlna, to prevent potential dependency conflicts.

To use mlna, ensure you have Python version 3.10 or higher installed. To install the package, run the following command in your terminal:

```
pip install git+https://github.com/Goli-SF/MLNA.git
```

# Usage
An internet connection is required to use mlna, as the package needs access to the Google Translate API for translating texts from other languages to English. Please avoid using a VPN while using this package, as it may disrupt the connection to the Google Translate API.

If you encounter the error messages `TypeError: 'NoneType' object is not iterable` or `TypeError: the JSON object must be str, bytes or bytearray, not NoneType` while using mlna, it indicates that the package was unable to access the Google Translate API due to internet connection issues or a problem with the API itself. In such cases, be patient and continue re-running your code until the error resolves and you receive an output.

This package assumes that the user already has a collection of machine-readable texts, potentially in various languages, some of which they may not understand. The primary purpose of mlna is to help users select the texts relevant to their research topic, without needing to translate all of them into languages they understand. Instead, users can first filter out the texts they need from their collection using the mlna package. Once the relevant texts are identified, they only need to translate those into a language they understand and perform a close reading.

To do this, follow these steps:

**1. Import the modules**

After installing the package, import its modules into your code:

```
from mlna import user_input, network
```

The `preproc` module runs in the background of these two modules. If you plan to use it independently for other tasks, you can also run:

```
from mlna import preproc
```

**2. Prepare text data**

Organize all the text documents you plan to work with into a table and convert it into a pandas DataFrame. The DataFrame must include the mandatory columns `text_id` and `full_text`, though you can add as many additional columns as needed. In the following examples, I will refer to this DataFrame as `text_df`.

**3. Choose entities**

Use the `get_entities` function in the `user_input` module to select the entities from your gathered texts that are relevant to your research:

```
entity_tags = user_input.get_entities()
```

This function presents a list of entities that the spaCy package can recognize within your texts. You can choose as many entities as needed by following the prompts provided by the function. It returns a list of entity tags, which are stored in the `entity_tags` variable in this example. These entity tags will help you identify relevant keywords within the texts stored in `text_df`, giving you an overview of the content of each text.

**4. Set user-defined entities**

If there are certain words that are not recognized as part of the entities you've selected but you still want them to be included in text searches and network visualizations, you can store them in a separate variable (other than `entity_tags`) and use them later in the network visualizations. For example, if you're interested in texts related to the development of the telegraph and telephone, you can store the words 'telegraph' and 'telephone' in a variable called `user_ents`:

```
user_ents = ['telegraph', 'telephone']
```

**5. Create a dictionary**

To extract the entities and words selected by the user from multilingual texts, the mlna package first translates them into English. However, proper names from non-English languages are often transliterated into English and may appear in various forms across different texts. Additionally, depending on the source language, these names might have different spellings. As a result, different spellings of the same entity may be recognized as distinct entities, even though they refer to the same thing, place or person. This can lead to incorrect representations of network relations between these names and other entities or words selected by the user in the network graph.

To address this issue, run the `make_user_dict` function from the `user_input` module. This function creates a dictionary that can be used in your script and also saves the dictionary as a pickled file in the directory of your code. This allows you to load the dictionary back into your script at any time and add more key-value pairs over time.

To create the dictionary, run:

```
user_dict = user_input.make_user_dict(text_df, entity_tags, user_ents=None, dict_path=None, threshold=80)
```

If you’ve decided to create a list of self-defined entities that are not recognized by the spaCy model, set `user_ents` in the code above to the `user_ents` list you created earlier.

If you provide a `dict_path`, the function will load an existing dictionary and add more key-value pairs to it. If you don't provide one, it will create a new dictionary from scratch. Regardless, the function will prompt you to decide whether you want to see groups of words that could potentially refer to the same entity.

* If you choose "yes," the function will show these word groups and ask you to specify a unified spelling for each group. These groups are identified using fuzzy matching. You can adjust the accuracy of the fuzzy matching by modifying the threshold value in the code above.

* If you choose "no," the function will prompt you to manually create key-value pairs. First, you'll need to provide a unified spelling for a certain entity, and then you’ll need to input all the different spellings that refer to that entity.

Make sure to run the `make_user_dict` function multiple times on the text dataframe. Here’s why:

For example, if you have the words 'Naser' and 'Naser al Din Qajar' and want to replace both with 'Nasser-al-Din Shah', the function will perform the following replacements:

Naser → Nasser-al-Din Shah

Naser al Din Qajar → Nasser-al-Din Shah

Now, if the package also detects 'Naser al Din' as an entity, but you forgot to include it as part of the keys for the 'Nasser-al-Din Shah' value, the dictionary will only replace 'Naser' with 'Nasser-al-Din Shah'. This would result in the name 'Nasser-al-Din Shah al Din', which is incorrect. If you spot such errors in the visualized network graph, run the `make_user_dict` function again and, in the case of this example, add the key-value pair `'Nasser-al-Din Shah al Din': 'Nasser-al-Din Shah'`. You can repeat this process as many times as necessary, ensuring all variations of the same entity name are unified.

**6. Visualize communities**

To visualize the communities within the collection of entities from `entity_tags` and maybe the words you've previously stored in `user_ents`, run the `detect_community` function from the `network` module:

```
network.detect_community(text_df, entity_tags, user_ents=None, user_dict=None, title='community_detection', figsize=(1000, 700), bgcolor='black', font_color='white')
```

This function generates a community visualization, which is saved in your code’s directory as a file named 'community_detection.html'. Open this file to interact with the community graph and explore the relationships between different nodes consisting of the extracted entities and the user-defined entities. You can customize the title of the .html file, its size, and the colors of the font and background directly in the function.

The `detect_community` function processes all the texts stored in the `text_df` DataFrame. provide the path to the dictionary in the `user_dict` argument.

If you notice any incorrect or duplicate spellings of a word or entity in the community graph and wish to correct them, simply run the `make_user_dict` function again and update your personalized user dictionary accordingly.

**7. Visualize network relations**

To visualize the network relations within the collection of entities from `entity_tags` (and potentially also the words stored in `user_ents`), run the `visualize_network` function from the `network` module. Be sure to update the values of `user_ents` and `user_dict` if they are not None:

```
netowrk.visualize_network(text_df, entity_tags, user_ents=None, user_dict=None, core=False, select_nodes=None, sources=None, title='network_visualization', figsize=(1000, 700), bgcolor='black', font_color='white')
```

This function generates a network graph, which is saved as 'network_visualization.html' in your code's directory. Open the file to interact with the network graph and explore the relationships between different nodes, which consist of the extracted entities and your selected words. Each relationship (edge) represents the co-occurrence of its nodes within a single sentence in the texts stored in `text_df`. You can customize the title, size, font color, and background color of the .html file in the function.

If you notice incorrect or duplicate spellings of a word or entity and want to correct them, run the `make_user_dict` function again and update your personalized user dictionary accordingly.

To view only the core of the network, set `core=True`. If you wish to visualize a network consisting of a specific group of nodes, store these nodes in a list and assign it to `select_nodes`. To ensure that the nodes you include in the `select_nodes` list actually exist in the network, generate the list using the `select_nodes` function from the `user_input` module:

```
select_nodes = user_input.select_nodes(text_df, entity_tags, user_ents=None, user_dict=None)
```

If you want to visualize the network using only certain texts from `text_df`, store the `text_id`s of these texts in the `sources` list.

**8. Select relevant texts**

After studying the network and community graphs, you should have a general overview of the subjects and correlations in the collection of texts. Now, it’s time to identify which nodes (entities) and edges (relationships between entities) appear in which texts in the collection. To do so, run the `filter_network_data` function from the `network` module:

```
filtered_df = network.filter_network_data(text_df, select_nodes, entity_tags, user_ents=None, user_dict=None, operator='OR')
```

* If you're interested in one or more nodes, set `operator='OR'`.

* If you're only interested in a specific edge (i.e., the co-occurrence of two nodes in one sentence), make sure `select_nodes` contains only those two nodes, and set `operator=AND`.

The output of this function is a dataframe containing the columns from your original dataframe, along with three additional columns containing network data: `source` and `target` (which will include one or both of your selected nodes, depending on whether you chose 'AND' or 'OR' as the operator) and `weight` (which indicates how many times a particular co-occurrence appears in each text).

You can now select the texts displayed in `filtered_df` and perform a close reading of them, knowing they likely contain information relevant to your research.

# Contributing

Contributions to the package, including bug fixes and new features, are welcome. When contributing to this repository, please first discuss the change you wish to make via a GitHub issue or email me before making a change.

# License
mlna has a GNU GPL license. For more detail, see the [LICENSE.md](https://github.com/Goli-SF/MLNA/blob/main/LICENSE.md) file. For the third-party licenses of other packages used for the development of mlna, see the [THIRD_PARTY_LICENSES.md](https://github.com/Goli-SF/MLNA/blob/main/THIRD_PARTY_LICENSES.md) file.

# Words of thanks
I hereby warmly thank Mariatta Wijaya for her insightful tips on CI and unit testing as well as Gaëtan Manchon for his helpful tips regarding the implementation of poetry.
