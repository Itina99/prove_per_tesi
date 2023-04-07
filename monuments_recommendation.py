import random
import numpy as np
import pandas as pd
from scipy import sparse
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

import lightfm
from lightfm.data import Dataset
from lightfm import LightFM, cross_validation
from lightfm.evaluation import precision_at_k, auc_score
from scipy.sparse import csr_matrix


def create_user_dict(df, name_col):
    user_dict = {}
    counter = 0
    for i in df[name_col].unique():
        user_dict[counter] = i
        counter += 1
    return user_dict


def create_item_dict(df, id_col, name_col):
    item_dict = {}
    for i in range(df.shape[0]):
        item_dict[(df.loc[i, id_col])] = df.loc[i, name_col]
    return item_dict


def create_feature_dict(features, ids):
    dict_features = []
    for i, f in zip(ids, features):
        dict_features.append({'mon_id': i, 'description': f})
    return dict_features


def get_descriptions_vec(df):
    tagged_desc = [TaggedDocument(doc, [i]) for i, doc in enumerate(df.description.values)]
    doc2vec_model = Doc2Vec(tagged_desc, vector_size=100, window=5, min_count=1, workers=4, epochs=20)
    desc_vectors = np.zeros((len(df.description.values), doc2vec_model.vector_size))
    for i in range(len(df.description.values)):
        desc_vectors[i] = doc2vec_model.dv[i]
    return desc_vectors


def sample_recommendation(mod, d, user_ids, features, df, user_dict):
    n_users, n_items = d.shape
    recommended_items = []
    for user_id in user_ids:
        if user_id not in user_dict.values():
            # cold start: recommend most popular items
            item_popularity = d.sum(axis=0).A1
            top_items = df['title'][np.argsort(-item_popularity)].values
            recommended_items = top_items[:5]
            print("User %s didn't have seen anything, we recommend the best monuments" % user_id)
            print("     Recommended:")
            for x in recommended_items:
                print("         %s" % x)

        else:
            known_positives = set(df['title'][d.tocsr()[user_id].indices])
            scores = mod.predict(user_id, np.arange(n_items), item_features=features)
            top_items = df['title'][np.argsort(-scores)].values
            recommended_items = []
            for item in top_items:
                if item not in known_positives:
                    recommended_items.append(item)
                if len(recommended_items) >= 5:
                    break

            print("User %s" % user_id)
            print("     Known positives:")
            for x in known_positives:
                print("         %s" % x)

            print("     Recommended:")
            for x in recommended_items:
                print("         %s" % x)

    return recommended_items



# item and user dict creation
df_playlist = pd.read_csv('data/user_ratings.csv', error_bad_lines=False, warn_bad_lines=False)
user_dict = create_user_dict(df_playlist, 'user_id')
df_item = pd.read_csv('data/monument_data_test.csv')
item_dict = create_item_dict(df=df_item, id_col='mon_id', name_col='title')

# processing description features with doc2vec
desc_vec = get_descriptions_vec(df_item)
dict_features = create_feature_dict(desc_vec, df_item.mon_id.values)

# dataset class
dataset = Dataset()
dataset.fit(users=df_playlist.user_id.values, items=df_item.mon_id.values)
dataset.fit_partial(items=df_item.mon_id.values, item_features=(tuple(x['description']) for x in dict_features))

# interaction and feature matrix creation
interactions = list(zip(df_playlist.user_id, df_playlist.monument_id))
(interaction, weights) = dataset.build_interactions(interactions)
item_features = dataset.build_item_features(((x['mon_id'], [tuple(x['description'])]) for x in dict_features))

# building the lightfm model
model = LightFM(loss='warp')
model.fit(interaction, item_features=item_features)
userid = 0
if random.randint(1, 10) <= 3:
    userid = random.choice(list(user_dict.keys()))
else:
    userid = 50
sample_recommendation(model, interaction, [userid], item_features, df_item, user_dict=user_dict)
