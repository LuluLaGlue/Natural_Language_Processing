import 'package:flutter/material.dart';
import 'package:greenbot/components/microphone_button.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'package:speech_to_text/speech_to_text.dart';

class MicrophoneScreen extends StatefulWidget {
  const MicrophoneScreen({Key? key}) : super(key: key);

  @override
  _MicrophoneScreenState createState() => _MicrophoneScreenState();
}

class _MicrophoneScreenState extends State<MicrophoneScreen> {
  final SpeechToText _speechToText = SpeechToText();
  bool _speechEnabled = false;
  String _lastWords = '';

  @override
  void initState() {
    super.initState();
    _initSpeech();
  }

  void _initSpeech() async {
    _speechEnabled = await _speechToText.initialize();
    setState(() {

    });
  }

  void _startListening() async {
    await _speechToText.listen(onResult: _onSpeechResult);
    setState(() {

    });
  }

  void _stopListening() async {
    await _speechToText.stop();
    setState(() {

    });
  }

  void _onSpeechResult(SpeechRecognitionResult result) {
    setState(() {
      _lastWords = result.recognizedWords;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Padding(
              padding: const EdgeInsets.only(top: 100, bottom: 50),
              child: MicrophoneButton(
                icon: Icon(
                  _speechToText.isNotListening
                    ? Icons.mic_off_outlined
                    : Icons.mic_none_rounded,
                  size: 70,
                ),
                onPressed: () {
                  _speechToText.isNotListening ? _startListening : _stopListening;
                },
              ),
            ),
            Expanded(
              child: Container(
                padding: const EdgeInsets.all(16),
                child: Text(
                  _speechToText.isListening
                    ? _lastWords
                    : _speechEnabled
                      ? 'Tap the microphone to start listening...'
                      : 'Speech not available',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
