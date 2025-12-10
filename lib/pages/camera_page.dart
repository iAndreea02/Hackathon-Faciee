import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

class CameraPage extends StatefulWidget {
  const CameraPage({super.key});

  @override
  State<CameraPage> createState() => _CameraPageState();
}

class _CameraPageState extends State<CameraPage> {
  CameraController? controller;
  Future<void>? initCam;

  @override
  void initState() {
    super.initState();
    initCam = _startCamera();
  }

  Future<void> _startCamera() async {
    final cams = await availableCameras();
    // Laptop Webcam = prima cameră găsită
    controller = CameraController(
      cams.first,
      ResolutionPreset.medium,
      enableAudio: false,
    );
    await controller!.initialize();
  }

  @override
  void dispose() {
    controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: FutureBuilder(
        future: initCam,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Center(
              child: CircularProgressIndicator(color: Colors.cyan),
            );
          }
          return Center(
            child: AspectRatio(
              aspectRatio: controller!.value.aspectRatio,
              child: CameraPreview(controller!),
            ),
          );
        },
      ),
    );
  }
}
