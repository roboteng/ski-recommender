from app import mtn_recommender, clean_df_for_recs, resort_stats_df

from flask import jsonify  # Flask, render_template, request
# import pickle
import pandas as pd
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.preprocessing import StandardScaler

PAYLOAD = "payload"
STATUS_CODE = "status_code"
RESORT = "resort"
TRAILS = "trails"
TRAIL = "trail"


def api_response(req, args, df=None, mtn_df=None):
    response = {PAYLOAD: {}, STATUS_CODE: "0"}
    if "apikey" in args:
        response[STATUS_CODE] = "200"
        if req == RESORT:
            resorts = []
            for resort in df[RESORT].unique():
                resorts.append(resort)
            response[PAYLOAD][RESORT] = resorts
        elif req == TRAILS:
            if RESORT in args:
                response[PAYLOAD][TRAILS] = {
                    trail.get("trail_name"): trail.get("colors")
                    for index, trail in (df[df[RESORT] == args[RESORT]]).iterrows()}
            else:
                response[PAYLOAD][TRAILS] = {
                    trail.get("trail_name"): trail.get("colors")
                    for index, trail in df.iterrows()}
        elif req == 'recommend':
            num_recs = args['num_recs'] if ('num_recs' in args) else 5
            index = df[(df[RESORT] == args[RESORT])
                       & (df['trail_name'] == args[TRAIL])].index()[0]
            row, recs = mtn_recommender(index, num_recs)
            results_df = pd.DataFrame(columns=[RESORT, 'resort_bottom', 'resort_top', 'greens', 'blues', 'blacks', 'bbs', 'lifts', 'price'])
            for rec in recs:
                results_df = results_df.append(resort_stats_df[resort_stats_df[RESORT] == rec])
            row = clean_df_for_recs(row)
        else:
            print('Unknown Req: {}'.format(req))
            response[STATUS_CODE] = '400'

    else:
        response[STATUS_CODE] = "401"
    return jsonify(response)
