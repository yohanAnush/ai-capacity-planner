#Model
model_path = "model/bayesian_regressor.p"

#Datasets
training_data = "dataset/dataset.csv"
data_path = "dataset/"

#Results
result_path = "results/"

# HTTP response codes
HTTP_200_OK = 200
HTTP_500_INTERNAL_SERVER_ERROR = 500
HTTP_503_SERVICE_UNAVAILABLE = 503
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_422_UNPROCESSABLE_ENTITY = 422

#Regressor Properties
DEFAULT_SAMPLE_COUNT=2000

#JSON KEYS
SAMPLE_COUNT="sample_count"
CONCURRENCY = "concurrency"
MESSAGE_SIZE = "message_size"
METHOD = "method"
SCENARIO = "scenario"
SAMPLING = "sampling"
NO_SAMPLING = "NS"
DEFAULT_METHOD = NO_SAMPLING