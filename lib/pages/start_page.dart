import 'package:flutter/material.dart';
import '../widgets/grid_painter.dart';
import '../widgets/logo_box.dart';

class StartPage extends StatelessWidget {
  const StartPage({super.key});

  static const Color bgStart = Color(0xFF0A0E1A);
  static const Color bgEnd = Color(0xFF001F30);
  static const Color accentPink = Color(0xFFE21ADB);
  static const Color accentCyan = Color(0xFF00E0FF);

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    /// Canvas design reference (width x height)
    const double refW = 480;
    const double refH = 800;

    /// Scaling factor so design matches tablet screen
    final double scaleW = size.width / refW;
    final double scaleH = size.height / refH;
    final double scale = (scaleW < scaleH) ? scaleW : scaleH;

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [bgStart, bgEnd],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: SafeArea(
          child: Center(
            child: SizedBox(
              width: refW * scale,
              height: refH * scale,
              child: Stack(
                children: [
                  /// background grid
                  Positioned.fill(
                    child: CustomPaint(
                      painter: GridPainter(
                        lineColor: accentCyan.withValues(alpha: 0.12),
                      ),
                    ),
                  ),

                  /// LOGO
                  Positioned(
                    top: 16 * scale,
                    left: 12 * scale,
                    child: LogoBox(scale: scale),
                  ),

                  /// TITLURI
                  Positioned(
                    top: 120 * scale,
                    left: 0,
                    right: 0,
                    child: Column(
                      children: [
                        Text(
                          "Hiello viitor student!",
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            color: accentPink,
                            fontSize: 38 * scale,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 1.2,
                          ),
                        ),
                        SizedBox(height: 6 * scale),
                        Text(
                          "Facultatea de Automatică, Calculatoare și Tehnologie",
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            color: accentCyan.withValues(alpha: 0.9),
                            fontSize: 16 * scale,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                  ),

                  /// IMAGINE ROBOT (CENTRU)
                  Positioned(
                    top: 230 * scale,
                    left: 40 * scale,
                    right: 40 * scale,
                    child: Image.asset(
                      "assets/robo.png",
                      height: 260 * scale,
                      fit: BoxFit.contain,
                    ),
                  ),

                  /// BUTON INTRARE
                  Positioned(
                    bottom: 120 * scale,
                    left: 60 * scale,
                    right: 60 * scale,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: accentPink,
                        padding: EdgeInsets.symmetric(vertical: 16 * scale),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(14),
                        ),
                      ),
                      onPressed: () =>
                          Navigator.pushNamed(context, '/camera'),
                      child: Text(
                        "Intră în aplicație",
                        style: TextStyle(
                          fontSize: 20 * scale,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),

                  /// HASH TAG
                  Positioned(
                    bottom: 18 * scale,
                    right: 14 * scale,
                    child: Text(
                      "#Hackathon 2025-2026",
                      style: TextStyle(
                        color: Colors.white.withValues(alpha: 0.12),
                        fontSize: 12 * scale,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
