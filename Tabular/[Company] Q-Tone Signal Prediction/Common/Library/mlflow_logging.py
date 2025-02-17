import mlflow
import pymysql
from mlflow.models.signature import infer_signature
from urllib.parse import urlparse
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
mlflow.set_tracking_uri('http://office.innerwave.co.kr:25000')
#mlflow.set_tracking_uri('mysql+pymysql://mlflow:mlflow!1234@surfinn.innerwave.co.kr:13306/mlflow')



#### 사용중 ######## 사용중 ######## 사용중 ######## 사용중 ####
def mlflow_logging(experiment, run_name, model, model_name, model_params_dict, metric_dict, tag, img_dict=None):
    mlflow.set_experiment(experiment)
    
    with mlflow.start_run(run_name=f'{run_name}') :

        #mlflow.sklearn.log_model(model, model_name)
        mlflow.log_params(model_params_dict)
        mlflow.log_metrics(metric_dict)
        #mlflow.log_artifacts(model)
        #mlflow.log_artifact("features.txt", artifact_path="features")


        # Fetch a specific artifact uri
        #artifact_uri = mlflow.get_artifact_uri(artifact_path="mlflow/artifacts/features.txt")

        if len(tag) >= 100 :
            mlflow.set_tag("colunms_error ", "The number of columns is too large.") 
        elif len(tag) < 100 :
            mlflow.set_tags(tag) 

def binary_classification_metric(y_true, y_prediction, y_prediction_proba):
    acc = accuracy_score(y_true, y_prediction)
    precision = precision_score(y_true, y_prediction)
    recall = recall_score(y_true, y_prediction)
    f1 = f1_score(y_true, y_prediction)
    try:
        auc = roc_auc_score(y_true, y_prediction)   
    except:    # 예외가 발생했을 때 실행됨
        auc = 1
        print('실측치가 1만 존재합니다.')
    return {'Accuracy':acc, 'Precision':precision, 'Recall':recall, 'F1_Score':f1, 'AUC':auc}


def multi_classification_metric(y_test, y_prediction, y_prediction_proba):
    acc = accuracy_score(y_test, y_prediction)
    precision = precision_score(y_test, y_prediction, average='weighted')
    recall = recall_score(y_test, y_prediction, average='weighted')
    f1 = f1_score(y_test, y_prediction, average='weighted')
    auc = roc_auc_score(y_test, y_prediction_proba, multi_class = 'ovr')
    return {'Accuracy':acc, 'Precision':precision, 'Recall':recall, 'F1_Score':f1, 'AUC':auc}


