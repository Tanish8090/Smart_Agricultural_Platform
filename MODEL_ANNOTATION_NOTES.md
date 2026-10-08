# Developer Note: Disease Model Annotation & Retraining Roadmap

**Project:** Smart Agriculture Platform (SAP)  
**Status:** Deferred to Future Phase (No Active Model Changes in Current Release)  
**Date:** October 2026  

---

## 1. Context & Teacher Recommendation
A recommendation was made by our project advisor/teacher to consider bounding-box / polygon annotation and targeted fine-tuning to further improve lesion localization and disease classification performance across edge conditions (e.g. partial leaf occlusion, varying sunlight/shadows, multi-disease co-infection).

---

## 2. Policy for Current Android App Release
Per strict project requirements for this targeted mobile UI polish release:
- **Zero Model Changes:** Existing ONNX models (`wheat.onnx`, `cotton.onnx`, `sugarcane.onnx`, `potato.onnx`, `rice.onnx`, `soybean.onnx`, `tomato.onnx`, `corn.onnx`, `apple.onnx`, `grape.onnx`, and `not_a_leaf.onnx`) remain 100% untouched.
- **Zero Architecture Changes:** Model architectures, input tensor dimensions ($224 \times 224 \times 3$), normalization ($[-1, 1]$ / ImageNet parameters), and ONNX opsets remain unchanged.
- **Zero Label Changes:** Output class mappings and diagnosis labels are fully preserved.
- **Zero Inference Code Changes:** Both JavaScript client-side ONNX Runtime Web and native Android `OnnxInferencePlugin` continue using the verified, production inference pipeline.

---

## 3. Recommended Future Annotation & Improvement Workflow
When the dedicated model-improvement phase is initiated, follow these systematic steps:

1. **Dataset Collection & Stratification:**
   - Gather localized agricultural dataset batches across key agro-climatic zones in India.
   - Separate field images by lighting conditions, growth stage, and common background interference (soil, farmer hands, weeds).

2. **Annotation Protocol:**
   - Use standard annotation platforms (e.g. CVAT, Label Studio, or Roboflow).
   - Annotate leaf regions of interest (ROI) and individual disease lesions (e.g. rust pustules, blight spots, rot areas).
   - Ensure explicit annotation of negative controls (healthy leaves, non-leaf farm objects, soil, boots, background vegetation).

3. **Training & Validation:**
   - Retrain or fine-tune models with data augmentation (random rotation, color jitter, affine transforms).
   - Validate using stratified k-fold cross-validation, checking precision, recall, and F1-score across all classes.

4. **ONNX Export & Quantization:**
   - Export optimized PyTorch/TensorFlow weights to ONNX format.
   - Run INT8 or FP16 quantization benchmarks to ensure inference speed remains under 100ms on mobile devices without accuracy degradation.

5. **Deployment & Verification:**
   - Verify byte parity and checksums before updating `models/` in `assets/models/` and `www/models/`.
