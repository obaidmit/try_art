import flask 
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = flask.Flask(__name__, template_folder='templates')

places = pd.read_csv('https://raw.githubusercontent.com/obaidmit/Recommendation-Datasets/main/data_content.csv', sep=',', encoding='latin-1',usecols=['title','category'])


count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(places['title'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

places = places.reset_index()
indices = pd.Series(places.index, index=places['title'])
all_titles = [places['title'][i] for i in range(len(places['title']))]


#FUNCTION THAT GET PLACES RECOMMENDATION BAESD ON THE COSINE SIMILARITY SCORES OF PLACES CATEGORY

def get_recommendations(title):
    cosine_sim= cosine_similarity(count_matrix,count_matrix)
    idx=indices[title]
    sim_scores= list(enumerate(cosine_sim[idx]))
    sim_scores= sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores= sim_scores[1:11]
    places_indices= [i[0] for i in sim_scores]
    tit= places['title'].iloc[places_indices]
    
    return_df = pd.DataFrame(columns=['Title'])
    return_df['Title'] = tit
    return return_df


    # Set up the main route
@app.route('/', methods=['GET', 'POST'])



def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))


    if flask.request.method == 'POST':
        pname = flask.request.form['place_names']
        pname = pname.title()
# check = difflib.get_close_matches(pname,all_titles,cutout=0.50,n=1)
        
        if pname not in all_titles:
            return(flask.render_template('negative.html', name = pname ))
        else:
            result_final = get_recommendations(pname)
            names = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
            return flask.render_template('positive.html', place_names = names, search_name = pname)

if __name__ == '__main__':
    app.debug = True
    app.run()
    