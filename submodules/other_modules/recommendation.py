
import pandas as pd
import numpy as np
from textblob import TextBlob
from sklearn.metrics.pairwise import cosine_similarity

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

def get_feature_words():
    return {
    'feature 1' :  ['service', 'experience', 'look', 'flavor', 'star', 'dish', 'store', 'tasty', 'come', 'return'],
    'feature 2' :  ['order', 'lunch' ,'dinner', 'enjoy', 'friend', 'breakfast', 'onion', 'soup','point', 'town'],
    'feature 3' :  ['eat', 'way', 'option', 'feel', 'portion', 'bowl', 'start', 'house', 'size','think'],
    'feature 4' :  ['visit', 'staff', 'night', 'serve', 'work', 'chip', 'change', 'let', 'counter','taste'],
    'feature 5' :  ['chicken', 'fry', 'sandwich', 'roll', 'bread', 'tender', 'make', 'shrimp','appetizer', 'grill'],
    'feature 6' :  ['time', 'year', 'spot', 'bit', 'couple', 'use', 'water', 'thank', 'treat', 'dog'],
    'feature 7' :  ['location', 'item', 'space', 'quality', 'share', 'stuff', 'plan', 'menu','favorite', 'trip'],
    'feature 8' :  ['place', 'day', 'wait', 'minute', 'choice', 'delivery', 'crispy', 'pay', 'tea','bite'],
    'feature 9' :  ['pizza', 'review', 'beer', 'parking', 'style', 'park', 'stop', 'street', 'plenty','walk'],
    'feature 10' :  ['restaurant', 'home', 'rice', 'ask', 'pork', 'need', 'dine', 'customer', 'pack','wine'],
    'feature 11' :  ['food', 'thing', 'lot', 'plate', 'cup', 'truck', 'taste', 'chain', 'juice','protein'],
    'feature 12' :  ['menu', 'meal', 'people', 'price', 'salad', 'potato', 'business', 'head','ingredient', 'reason'],
    'feature 13' :  ['seat', 'hour', 'pick', 'piece', 'half', 'person', 'course', 'grab', 'deal','note'],
    'feature 14' :  ['bar', 'table', 'drink', 'sit', 'cook', 'fun', 'tell', 'steak', 'honey', 'cold'],
    'feature 15' :  ['try', 'love', 'area', 'room', 'dessert', 'kind', 'reservation', 'locate', 'miss','manager'],
    'feature 16' :  ['cheese', 'end', 'slice', 'husband', 'bring', 'pie', 'crust', 'sweet', 'base','group'],
    'feature 17' :  ['coffee', 'egg', 'bacon', 'tomato', 'cake', 'mushroom', 'pepper', 'sausage','pickle', 'mix'],
    'feature 18' :  ['sauce', 'drive', 'family', 'door', 'today', 'touch', 'heat', 'distance', 'boy','face'],
    'feature 19' :  ['meat', 'line', 'beef', 'bun', 'wall', 'morning', 'establishment', 'phone', 'pub','stand'],
    'feature 20' :  ['spicy', 'hand', 'mask', 'super', 'car', 'window', 'purchase', 'toast', 'kitchen','sign'],
    }

def extract_sentences_with_features(text, feature_words):
    stopwords_set = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    def preprocess_token(token):
        token = token.lower()
        token = lemmatizer.lemmatize(token)
        return token

    def preprocess_sentence(sentence):
        tokens = word_tokenize(sentence)
        tokens = [preprocess_token(token) for token in tokens if token.isalpha()]
        tokens = [token for token in tokens if token not in stopwords_set]
        return tokens

    preprocessed_text = [preprocess_sentence(sentence) for sentence in sent_tokenize(text)]

    relevant_sentences = {}
    for feature_word, related_words in feature_words.items():
        relevant_sentences[feature_word] = []
        for sentence_tokens in preprocessed_text:
            if any((feature_word in sentence_tokens) or (related_word in sentence_tokens) for related_word in related_words):
                relevant_sentences[feature_word].append(' '.join(sentence_tokens))

    return relevant_sentences

def get_feature_df(df, feature_words):
    df['feature_summaries'] = df['review'].apply(lambda x: extract_sentences_with_features(x, feature_words))

    for index, row in df.iterrows():
        relevant_sentences = row['feature_summaries']
        dic = {}
        for feature_word, sentences in relevant_sentences.items():
            joined_sentence = ' '.join(sentences)
            dic[feature_word] = joined_sentence
        df.at[index, 'feature_summaries'] = dic

    return df

def calculate_sentiment_score(sentence):
    blob = TextBlob(sentence)
    return blob.sentiment.polarity

def get_rec_dfs(df_sent):
    df_user_res_grp = df_sent.groupby(["business_id", "user_id"]).apply(lambda x: x[x != 0].mean(numeric_only=True))
    df_user_res_grp.reset_index(inplace=True)
    df_user_res_grp.fillna(0.0, inplace=True)

    df_sent_user = df_sent.drop(columns=["business_id"])
    df_user_grp = df_sent_user.groupby(["user_id"]).apply(lambda x: x.abs()[x != 0].mean(numeric_only=True))
    df_user_grp.reset_index(inplace=True)
    df_user_grp.fillna(0.0, inplace=True)

    df_sent_res = df_sent.drop(columns=["user_id"])
    df_res_grp = df_sent_res.groupby(["business_id"]).apply(lambda x: x[x != 0].mean(numeric_only=True))
    df_res_grp.reset_index(inplace=True)
    df_res_grp.fillna(0.0, inplace=True)

    return df_user_res_grp, df_user_grp, df_res_grp

def collaborative_filtering(target_user, df_user_res_grp, df_user_grp, features, similarity_threshold=0.7):
    selected_user_df = df_user_grp[df_user_grp['user_id'] == target_user]
    sel_usr_zro_cols = selected_user_df.columns[selected_user_df.eq(0).any()].tolist()
    sel_usr_features = selected_user_df[features].columns[selected_user_df[features].any()]

    selected_user_features = df_user_grp.loc[df_user_grp['user_id'] == target_user, sel_usr_features].values

    user_features = df_user_grp[sel_usr_features].values

    user_similarity_matrix = cosine_similarity(selected_user_features, user_features)

    similarity_df = pd.DataFrame({
        'user_id': df_user_grp['user_id'],
        'similarity_score': user_similarity_matrix.flatten()
    })
    similarity_df = similarity_df.sort_values('similarity_score', ascending=False)

    similarity_df = similarity_df.drop(similarity_df[similarity_df['user_id'] == target_user].index)

    similar_users = similarity_df[similarity_df['similarity_score'] > similarity_threshold]

    filtered_user_ids = similar_users['user_id'].tolist()

    df_user_res_wt_sim = pd.merge(df_user_res_grp, similar_users, on='user_id')
    df_user_res_wt_sim = df_user_res_wt_sim.drop(columns=sel_usr_zro_cols)
    df_user_res_wt_sim[sel_usr_features] = df_user_res_wt_sim[sel_usr_features].mul(df_user_res_wt_sim['similarity_score'], axis=0)

    aggregated_ratings = df_user_res_wt_sim[df_user_res_wt_sim['user_id'].isin(filtered_user_ids)].groupby('business_id')[sel_usr_features].apply(lambda x: x[x != 0].mean())
    aggregated_ratings.fillna(0.0, inplace=True)

    predicted_ratings_scr = aggregated_ratings.apply(lambda x: x[x != 0].mean(), axis=1)
    predicted_ratings_scr = predicted_ratings_scr.dropna()

    normalized_ratings = (predicted_ratings_scr - predicted_ratings_scr.min()) / (predicted_ratings_scr.max() - predicted_ratings_scr.min()) * 4 + 1

    all_businesses = normalized_ratings.sort_values(ascending=False)

    df_cf = pd.DataFrame({'business_id': all_businesses.index, 'cf_predicted_rating': all_businesses.values})

    return df_cf

def content_based_filtering(df_user_grp, df_res_grp, target_user):
    selected_user_preferences = df_user_grp.loc[df_user_grp['user_id'] == target_user].drop('user_id', axis=1)

    similarity_scores = cosine_similarity(selected_user_preferences, df_res_grp.drop('business_id', axis=1))

    df_cbf = pd.DataFrame({
        'business_id': df_res_grp['business_id'],
        'similarity_score': similarity_scores.flatten()
    })

    min_score = df_cbf['similarity_score'].min()
    max_score = df_cbf['similarity_score'].max()

    df_cbf['cbf_predicted_rating'] = 1 + (df_cbf['similarity_score'] - min_score) * (5 - 1) / (max_score - min_score)
    df_cbf = df_cbf.drop('similarity_score', axis=1)

    df_cbf = df_cbf.sort_values('cbf_predicted_rating', ascending=False).reset_index(drop=True)

    return df_cbf

def hybrid_recommendation(colab_df, content_df, content_weight, collab_filtering_weight, n_recommendations):
    hy_df = pd.merge(content_df, colab_df, on='business_id')

    hy_df['weighted_hybrid_score'] = hy_df['cbf_predicted_rating'] * content_weight + hy_df['cf_predicted_rating'] * collab_filtering_weight

    ranked_business_ids = hy_df.sort_values(by='weighted_hybrid_score', ascending=False)['business_id'].head(n_recommendations).tolist()
    return ranked_business_ids

def recommendation(user_id, df, n_restaurants=10):
    df = df.drop(columns=['categories','address', 'state_', 'city', 'postal_code', 'latitude', 'longitude', 'stars', 'review_count', 'is_open', 'hours', 'review_id', 'useful', 'funny', 'cool', 'date_', 'name' ])
    df = df.rename(columns={'text_': 'review'})
    df = df.dropna()
    df = df.drop_duplicates()

    feature_words = get_feature_words()

    df_sent = get_feature_df(df, feature_words)

    feature_name_list = list(df_sent['feature_summaries'][0].keys())

    df_sent["sentiment_scores"] = df_sent["feature_summaries"].apply(lambda row: {feature: calculate_sentiment_score(sentence) for feature, sentence in row.items()})
    sentiment_scores_df = pd.DataFrame(df_sent["sentiment_scores"].tolist())
    df_sent = pd.concat([df_sent, sentiment_scores_df], axis=1)
    df_sent = df_sent.drop(columns=[ 'review', 'feature_summaries', 'sentiment_scores'])

    df_user_res_feature_scr, df_user_feature_scr, df_res_feature_scr = get_rec_dfs(df_sent)

    cf_df = collaborative_filtering(target_user=user_id, df_user_res_grp=df_user_res_feature_scr, df_user_grp=df_user_feature_scr, features=feature_name_list, similarity_threshold=0.7)
    cbf_df = content_based_filtering(df_user_grp=df_user_feature_scr, df_res_grp=df_res_feature_scr, target_user=user_id)

    ranked_rest_ids = hybrid_recommendation(colab_df=cf_df, content_df=cbf_df, content_weight=0.5, collab_filtering_weight=0.5, n_recommendations=n_restaurants)

    return ranked_rest_ids



# Run this
path = '/content/drive/MyDrive/FYP/data/post20by20.csv'
df = pd.read_csv(path)

result = recommendation('sbcPtUZ9gKmwQ4LnP8udew', df, 10)
result