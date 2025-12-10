import 'package:flutter/material.dart';

class LogoBox extends StatelessWidget {
  final double scale;
  const LogoBox({required this.scale});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(6 * scale),
      decoration: BoxDecoration(
        color: const Color(0xFF0E2038),
        borderRadius: BorderRadius.circular(10 * scale),
      ),
      child: Image.asset(
        'assets/logo.png',
        width: 64 * scale,
        height: 64 * scale,
      ),
    );
  }
}
