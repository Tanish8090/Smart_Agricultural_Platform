package com.sap.agri;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.util.Log;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.annotation.Permission;
import com.getcapacitor.annotation.PermissionCallback;

import java.util.ArrayList;
import java.util.Locale;

@CapacitorPlugin(
    name = "VoiceRecognition",
    permissions = {
        @Permission(
            alias = "microphone",
            strings = { Manifest.permission.RECORD_AUDIO }
        )
    }
)
public class VoiceRecognitionPlugin extends Plugin {

    private static final String TAG = "VoiceRecognitionPlugin";
    private SpeechRecognizer speechRecognizer;
    private PluginCall activeCall;
    private boolean isListening = false;

    @PluginMethod
    public void isAvailable(PluginCall call) {
        boolean available = SpeechRecognizer.isRecognitionAvailable(getContext());
        JSObject ret = new JSObject();
        ret.put("available", available);
        call.resolve(ret);
    }

    @PluginMethod
    public void startListening(PluginCall call) {
        if (!SpeechRecognizer.isRecognitionAvailable(getContext())) {
            call.reject("UNAVAILABLE", "Speech recognition is not available on this device.");
            return;
        }

        if (getPermissionState("microphone") != com.getcapacitor.PermissionState.GRANTED) {
            requestPermissionForAlias("microphone", call, "microphoneCallback");
            return;
        }

        startListeningInternal(call);
    }

    @PermissionCallback
    private void microphoneCallback(PluginCall call) {
        if (getPermissionState("microphone") == com.getcapacitor.PermissionState.GRANTED) {
            startListeningInternal(call);
        } else {
            call.reject("PERMISSION_DENIED", "Microphone permission denied");
        }
    }

    private void startListeningInternal(PluginCall call) {
        final String language = call.getString("language", "hi-IN");

        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                try {
                    // Cancel any previous session
                    cleanupRecognizer();

                    activeCall = call;
                    speechRecognizer = SpeechRecognizer.createSpeechRecognizer(getContext());
                    speechRecognizer.setRecognitionListener(new RecognitionListener() {
                        @Override
                        public void onReadyForSpeech(Bundle params) {
                            isListening = true;
                            Log.d(TAG, "Native SpeechRecognizer ready for speech");
                        }

                        @Override
                        public void onBeginningOfSpeech() {
                            Log.d(TAG, "Native SpeechRecognizer user began speaking");
                        }

                        @Override
                        public void onRmsChanged(float rmsdB) {}

                        @Override
                        public void onBufferReceived(byte[] buffer) {}

                        @Override
                        public void onEndOfSpeech() {
                            Log.d(TAG, "Native SpeechRecognizer end of speech detected");
                        }

                        @Override
                        public void onError(int error) {
                            Log.w(TAG, "Native SpeechRecognizer error code: " + error);
                            isListening = false;

                            if (activeCall != null) {
                                if (error == SpeechRecognizer.ERROR_NO_MATCH || error == SpeechRecognizer.ERROR_SPEECH_TIMEOUT) {
                                    activeCall.reject("NO_SPEECH", "No speech detected");
                                } else if (error == SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS) {
                                    activeCall.reject("PERMISSION_DENIED", "Microphone permission denied");
                                } else {
                                    activeCall.reject("SPEECH_ERROR", "Speech recognition failed with code: " + error);
                                }
                                activeCall = null;
                            }
                            cleanupRecognizer();
                        }

                        @Override
                        public void onResults(Bundle results) {
                            isListening = false;
                            ArrayList<String> matches = results != null ? results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION) : null;
                            String transcript = (matches != null && !matches.isEmpty()) ? matches.get(0) : "";

                            Log.d(TAG, "Native SpeechRecognizer result transcript: " + transcript);

                            if (activeCall != null) {
                                if (transcript == null || transcript.trim().isEmpty()) {
                                    activeCall.reject("NO_SPEECH", "No speech recognized");
                                } else {
                                    JSObject ret = new JSObject();
                                    ret.put("status", "success");
                                    ret.put("transcript", transcript.trim());
                                    activeCall.resolve(ret);
                                }
                                activeCall = null;
                            }
                            cleanupRecognizer();
                        }

                        @Override
                        public void onPartialResults(Bundle partialResults) {}

                        @Override
                        public void onEvent(int eventType, Bundle params) {}
                    });

                    Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                    intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);

                    // Language tags: 'hi-IN' or 'en-IN' with 'en-US' fallback
                    if (language != null && language.toLowerCase().contains("hi")) {
                        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "hi-IN");
                        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, "hi-IN");
                        intent.putExtra(RecognizerIntent.EXTRA_ONLY_RETURN_LANGUAGE_PREFERENCE, "hi-IN");
                    } else {
                        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "en-IN");
                        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, "en-IN");
                    }

                    intent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3);
                    intent.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, false);

                    speechRecognizer.startListening(intent);

                } catch (Exception e) {
                    Log.e(TAG, "Error starting speech recognition", e);
                    isListening = false;
                    if (activeCall != null) {
                        activeCall.reject("START_FAILED", e.getMessage());
                        activeCall = null;
                    }
                    cleanupRecognizer();
                }
            }
        });
    }

    @PluginMethod
    public void stopListening(PluginCall call) {
        getActivity().runOnUiThread(new Runnable() {
            @Override
            public void run() {
                try {
                    if (speechRecognizer != null) {
                        speechRecognizer.stopListening();
                    }
                } catch (Exception ignored) {}

                isListening = false;
                JSObject ret = new JSObject();
                ret.put("status", "stopped");
                call.resolve(ret);
            }
        });
    }

    private void cleanupRecognizer() {
        if (speechRecognizer != null) {
            try {
                speechRecognizer.destroy();
            } catch (Exception ignored) {}
            speechRecognizer = null;
        }
        isListening = false;
    }

    @Override
    protected void handleOnDestroy() {
        cleanupRecognizer();
        super.handleOnDestroy();
    }
}
