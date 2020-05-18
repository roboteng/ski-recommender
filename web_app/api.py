from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

PAYLOAD = "payload"
STATUS_CODE = "status_code"


def api_response(req, args, df=None, mtn_df=None):
    response = {PAYLOAD: {}, STATUS_CODE: "0"}
    if "apikey" in args:
        response[STATUS_CODE] = "200"
        if req == "resorts":
            resorts = []
            for resort in df['resort'].unique():
                resorts.append(resort)
            response[PAYLOAD]["resorts"] = resorts
        elif req == "trails":
            if "resort" in args:
                response[PAYLOAD]['trails'] = list(df[df['resort'] == args['resort']]["trail_name"])
            else:
                response[PAYLOAD]["trails"] = list(df["trail_name"])

    else:
        response[STATUS_CODE] = "401"
    return jsonify(response)
