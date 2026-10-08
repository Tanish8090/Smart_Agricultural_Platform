package com.sap.agri;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraManager;
import android.util.Log;

import androidx.core.content.ContextCompat;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.annotation.Permission;
import com.getcapacitor.annotation.PermissionCallback;

@CapacitorPlugin(
    name = "CameraBridge",
    permissions = {
        @Permission(
            alias = "camera",
            strings = { Manifest.permission.CAMERA }
        )
    }
)
public class CameraBridgePlugin extends Plugin {

    private static final String TAG = "CameraBridgePlugin";

    @PluginMethod
    public void checkCameraPermission(PluginCall call) {
        boolean granted = ContextCompat.checkSelfPermission(getContext(), Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED;
        JSObject ret = new JSObject();
        ret.put("granted", granted);
        call.resolve(ret);
    }

    @PluginMethod
    public void requestCameraPermission(PluginCall call) {
        if (ContextCompat.checkSelfPermission(getContext(), Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
            JSObject ret = new JSObject();
            ret.put("granted", true);
            call.resolve(ret);
            return;
        }

        requestPermissionForAlias("camera", call, "cameraPermissionCallback");
    }

    @PermissionCallback
    private void cameraPermissionCallback(PluginCall call) {
        boolean granted = ContextCompat.checkSelfPermission(getContext(), Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED;
        if (granted) {
            JSObject ret = new JSObject();
            ret.put("granted", true);
            call.resolve(ret);
        } else {
            call.reject("CAMERA_PERMISSION_DENIED", "Camera permission denied by user");
        }
    }

    @PluginMethod
    public void isCameraAvailable(PluginCall call) {
        try {
            CameraManager manager = (CameraManager) getContext().getSystemService(Context.CAMERA_SERVICE);
            if (manager == null) {
                JSObject ret = new JSObject();
                ret.put("available", false);
                ret.put("count", 0);
                call.resolve(ret);
                return;
            }

            String[] cameraIds = manager.getCameraIdList();
            boolean hasBack = false;
            boolean hasFront = false;

            for (String id : cameraIds) {
                CameraCharacteristics characteristics = manager.getCameraCharacteristics(id);
                Integer facing = characteristics.get(CameraCharacteristics.LENS_FACING);
                if (facing != null) {
                    if (facing == CameraCharacteristics.LENS_FACING_BACK) {
                        hasBack = true;
                    } else if (facing == CameraCharacteristics.LENS_FACING_FRONT) {
                        hasFront = true;
                    }
                }
            }

            JSObject ret = new JSObject();
            ret.put("available", cameraIds.length > 0);
            ret.put("count", cameraIds.length);
            ret.put("hasBackCamera", hasBack);
            ret.put("hasFrontCamera", hasFront);
            call.resolve(ret);

        } catch (Exception e) {
            Log.e(TAG, "Error checking camera availability", e);
            call.reject("CAMERA_CHECK_FAILED", e.getMessage());
        }
    }
}
