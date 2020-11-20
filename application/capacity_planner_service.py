import numbers

from flask import Flask
from flask import request, jsonify, Response
from application.regressor import load_model, predict_point, predict_list, max_tps
import application.constants as const
from application.response_formatter import formatter, json_value_validator

from multiprocessing import Process

ai_capacity_planner = Flask(__name__)

# Load Model
load_model();


@ai_capacity_planner.route('/')
def check():
    return Response(status=const.HTTP_200_OK)


# @ai_capacity_planner.route('/poly_predict_list', methods=['POST'])
# def poly_predict_list():
#     data = request.get_json()
#     sample_count = 2000
#
#     start_time = time.time()
#
#     if data['method'] == "sampling":
#         try:
#             sample_count = data['sample_count']
#             file_name = data['file_name']
#             predict_list(sample_count=sample_count, file_name=file_name);
#         except:
#             print('Sample Count Not Defined/File Error')
#
#     else:
#         try:
#             file_name = data['file_name']
#             predict_list(method="NS", sample_count=sample_count, file_name=file_name);
#         except:
#             print('File Error')
#
#     print("--- %s seconds for Prediction ---" % (time.time() - start_time))
#     return 'Prediction Complete';


@ai_capacity_planner.route('/predict_point', methods=['POST'])
def point_prediction():
    if request.method == "POST":
        data = request.get_json()

        method = const.DEFAULT_METHOD
        sample_count = const.DEFAULT_SAMPLE_COUNT

        try:
            scenario = data['scenario'].capitalize();
            concurrency = data['concurrency']
            message_size = data['message_size']
            if not (json_value_validator(scenario=scenario,concurrency=concurrency,message_size=message_size, type="point_pred")):
                return Response(status=const.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            print(e)
            return Response(status=const.HTTP_422_UNPROCESSABLE_ENTITY)

        if "method" in data:
            if data['method'] == "sampling":
                method = "sampling"
                try:
                    if not (data.get('sample_count') is None):
                        sample_count = data['sample_count']
                        if not (json_value_validator(sample_count=sample_count, type="sampling_check")):
                            return Response(status=const.HTTP_405_METHOD_NOT_ALLOWED)
                except:
                    return Response(status=const.HTTP_422_UNPROCESSABLE_ENTITY)

            elif data['method'] == "NS":
                    method = "NS"

        try:
            prediction = predict_point([scenario, concurrency, message_size], method=method, sample_count=sample_count);
            tps,latency = formatter(tps=prediction, concurrency=concurrency);

            return jsonify(
                tps=tps,
                latency=latency
            )
        except:
            print("Error")
            return Response(status=const.HTTP_422_UNPROCESSABLE_ENTITY)

@ai_capacity_planner.route('/max_tps', methods=['POST'])
def max_tps_prediction():
    if request.method == "POST":
        data = request.get_json()

        method = const.DEFAULT_METHOD
        sample_count = const.DEFAULT_SAMPLE_COUNT

        try:
            scenario = data['scenario'].capitalize();
            message_size = data['message_size']
            if not (json_value_validator(scenario=scenario,message_size=message_size, type="max_tps")):
                return Response(status=const.HTTP_405_METHOD_NOT_ALLOWED)
        except:
            return Response(status=const.HTTP_422_UNPROCESSABLE_ENTITY)

        if "method" in data:
            if data['method'] == "sampling":
                method = "sampling"
                try:
                    if not (data.get('sample_count') is None):
                        sample_count = data['sample_count']
                        if not (json_value_validator(sample_count=sample_count, type="sampling_check")):
                            return Response(status=const.HTTP_405_METHOD_NOT_ALLOWED)
                except Exception as e:
                    print(e)
                    return Response(status=const.HTTP_422_UNPROCESSABLE_ENTITY)

            elif data['method'] == "NS":
                method = "NS"

        try:
            tps = max_tps([scenario, message_size], method=method, sample_count=sample_count)
            tps = formatter(tps=tps);

            return jsonify(
                max_tps=tps,
            )

        except:
            print("Error")
            return Response(status=const.HTTP_422_UNPROCESSABLE_ENTITY)

if __name__ == '__main__':
    ai_capacity_planner.run()
