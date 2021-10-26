import 'package:flutter/material.dart';

class MicrophoneButton extends StatelessWidget {
  const MicrophoneButton({
    Key? key,
    required this.onPressed,
    required this.icon,
  }) : super(key: key);

  final VoidCallback onPressed;
  final Icon icon;

  @override
  Widget build(BuildContext context) {
    return TextButton(
      child: icon,
      style: TextButton.styleFrom(
        primary: const Color(0xff4dd893),
        side: const BorderSide(color: Color(0xff4dd893), width: 4),
        shape: const CircleBorder(),
        minimumSize: const Size(200, 200),
      ),
      onPressed: () {

      },
    );
  }
}
