import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:greenbot/screens/microphone_screen.dart';

void main() {
  runApp(const IAOnEstLa());
}

class IAOnEstLa extends StatelessWidget {
  const IAOnEstLa({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersive);
    return const MaterialApp(
        debugShowCheckedModeBanner: false,
        home: Scaffold(
          backgroundColor: Color(0xff2e2f31),
          body: Center(
            child: MicrophoneScreen(),
          ),
        )
    );
  }
}