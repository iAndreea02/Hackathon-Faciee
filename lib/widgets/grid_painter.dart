import 'package:flutter/material.dart';

class GridPainter extends CustomPainter {
  final Color lineColor;
  const GridPainter({required this.lineColor});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = lineColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1;

    const rows = 8;
    const cols = 12;

    for (int r = 0; r <= rows; r++) {
      final y = size.height * (r / rows) * 0.9 + size.height * 0.05;
      canvas.drawLine(
          Offset(size.width * 0.05, y), Offset(size.width * 0.95, y), paint);
    }
    for (int c = 0; c <= cols; c++) {
      final x = size.width * (c / cols) * 0.9 + size.width * 0.05;
      canvas.drawLine(
          Offset(x, size.height * 0.05), Offset(x, size.height * 0.95), paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
