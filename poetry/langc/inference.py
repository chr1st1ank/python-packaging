from typing import Tuple
import onnxruntime
import numpy as np


def init_onnx_session(model_path) -> onnxruntime.InferenceSession:
    """Initializes the onnx model"""
    sess_options = onnxruntime.SessionOptions()
    sess_options.intra_op_num_threads = 1
    sess_options.execution_mode = onnxruntime.ExecutionMode.ORT_SEQUENTIAL
    sess_options.graph_optimization_level = (
        onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
    )
    onnx_session = onnxruntime.InferenceSession(model_path, sess_options)
    return onnx_session


def predict_language(onnx_session, input_string: str) -> Tuple[str, float]:
    """Runs a prediction using the onnx model and returns the most likely label and confidence"""
    pred_onx = onnx_session.run(
        None, {"string_input": np.array([input_string]).reshape(1, 1)}
    )
    label = pred_onx[0][0]
    probas = pred_onx[1][0]

    return label, probas[label]
