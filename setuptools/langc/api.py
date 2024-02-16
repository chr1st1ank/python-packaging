import importlib.resources
from bottle import route, run

from .inference import init_onnx_session, predict_language

onnx_session = None


@route("/guess/<text>")
def guess(text):
    language, confidence = predict_language(onnx_session, text)
    return {"language": language, "confidence": confidence}


def main():
    global onnx_session
    import sys

    print(sys.executable)
    with importlib.resources.path("langc.models", "classifier.onnx") as model_path:
        onnx_session = init_onnx_session(model_path)

    run(host="0.0.0.0", port=8080)
