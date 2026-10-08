package com.sap.agri;

import android.os.Bundle;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(OnnxInferencePlugin.class);
        registerPlugin(VoiceRecognitionPlugin.class);
        registerPlugin(CameraBridgePlugin.class);
        super.onCreate(savedInstanceState);
    }

    @Override
    public void onBackPressed() {
        if (bridge != null && bridge.getWebView() != null) {
            bridge.getWebView().evaluateJavascript(
                "(function() { return (typeof window.handleAndroidHardwareBack === 'function') ? window.handleAndroidHardwareBack() : false; })()",
                result -> {
                    if (!"true".equals(result)) {
                        runOnUiThread(() -> MainActivity.super.onBackPressed());
                    }
                }
            );
        } else {
            super.onBackPressed();
        }
    }
}
