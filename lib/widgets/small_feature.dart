import 'package:flutter/material.dart';

class SmallFeature extends StatelessWidget {
  final IconData icon;
  final String label;

  const SmallFeature({required this.icon, required this.label});

  @override
  Widget build(BuildContext context) {
    final scale = (MediaQuery.of(context).size.shortestSide / 360);

    return Column(
      children: [
        Icon(icon, size: 28 * scale, color: Colors.white70),
        SizedBox(height: 6 * scale),
        Text(label, style: TextStyle(color: Colors.white60, fontSize: 12 * scale)),
      ],
    );
  }
}
