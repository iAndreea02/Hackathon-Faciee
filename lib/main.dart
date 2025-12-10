import 'package:flutter/material.dart';
import 'pages/start_page.dart';
import 'pages/camera_page.dart';

void main() {
  runApp(const ACIEEApp());
}

class ACIEEApp extends StatelessWidget {
  const ACIEEApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PROVOCARE 2025 - ACIEE',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        useMaterial3: true,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const StartPage(),
        '/camera': (context) => const CameraPage(),
      },
    );
  }
}
