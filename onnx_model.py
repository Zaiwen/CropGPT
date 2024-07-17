import onnxruntime as ort
import numpy as np

# 初始化ONNX运行时，并加载ONNX模型
ort_session = ort.InferenceSession("model.onnx")

def one_hot(seq):
    seq = seq.strip().upper()
    alphabet = 'ACGT'
    char_to_int = dict((c, i) for i, c in enumerate(alphabet))
    integer_encoded = [char_to_int[char] for char in seq if char in char_to_int]
    one_hot_encoded = []
    for value in integer_encoded:
        letter = [0 for _ in range(len(alphabet))]
        letter[value] = 1
        one_hot_encoded.append(letter)
    return one_hot_encoded


def preprocess(input_sequence):
    encoded_seq = one_hot(input_sequence)
    # 直接将编码后的序列转换为numpy数组，假设模型可以接受任意长度的序列
    return np.array([encoded_seq], dtype=np.float32)


def predict_with_onnx(input_sequences):
    predictions = []
    for input_sequence in input_sequences:
        processed_data = preprocess(input_sequence) 
        inputs = {ort_session.get_inputs()[0].name: processed_data}
        ort_outs = ort_session.run(None, inputs)
        prediction = ort_outs[0][0]
        predictions.append(ort_outs)
        # predictions.append(prediction)
    return predictions


if __name__ == "__main__":
    sequences = ['TGAGTGAAGGCAGAATTGACCCATGCAGCTTCCTTTCTTTCACCACTCACTTGCTAGGAAACTACAAAAATAGAAAAAGAAAACTCACGGCAACCAAAAACGCGAACTCCTAGAGGGTTTCGAACACTTTGAAATTTGTATCAGACATCAAATGAAATCTTTAACTTCTT']
    predictions = predict_with_onnx(sequences)
    print(predictions)



