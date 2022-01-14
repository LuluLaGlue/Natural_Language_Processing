import 'dart:convert';
import 'dart:ffi';

import 'package:aia/pathResult.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:http/http.dart' as http;

import 'models/Path.dart';

void main() {
  runApp(MyApp());
}



class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Flutter Demo',
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final SpeechToText _speechToText = SpeechToText();
  bool _speechEnabled = false;
  String _lastWords = '';
  List<Path> paths = [];
  String error = '';
  String errorInfos = '';
  bool is_loading = false;

  @override
  void initState() {
    super.initState();
    _initSpeech();
  }

  /// This has to happen only once per app
  void _initSpeech() async {
    _speechEnabled = await _speechToText.initialize();
    setState(() {});
  }

  /// Each time to start a speech recognition session
  void _startListening() async {
    await _speechToText.listen(onResult: _onSpeechResult, localeId: 'fr_FR');
    setState(() {});
  }

  /// Manually stop the active speech recognition session
  /// Note that there are also timeouts that each platform enforces
  /// and the SpeechToText plugin supports setting timeouts on the
  /// listen method.
  void _stopListening() async {
    await _speechToText.stop();
    setState(()  {
    });
  }

  Future<List<Path>> getPathsFromText(String text) async {
    List<Path> paths = <Path>[];
    http.Response response = await sendSpeechResult(text);
    if (response.statusCode == 200) {
      Map<String, dynamic> data = jsonDecode(response.body);

      if (data['error'] != null) {
        if (data['error'] is String) {
          error = data['error'];
        }
        if (data['info'] is String) {
          errorInfos = data['info'];
        }
        return paths;
      } else {
        List<dynamic> jsonPaths = data['path'];
        for (var path in jsonPaths) {
          paths.add(Path.fromJson(path));
        }
        return paths;
      }
    } else {
      // throw Exception('Failed to get Path.');
      return paths;
    }
  }
  /// This is the callback that the SpeechToText plugin calls when
  /// the platform returns recognized words.
  void _onSpeechResult(SpeechRecognitionResult result) async {
    setState(() {
      _lastWords = result.recognizedWords;
    });
    // developper.log()
  }

  Future<http.Response> sendSpeechResult(String text) {
    String body = jsonEncode(<String, String>{
      'query': text,
    });
    return http.post(
      Uri.parse('https://api-aia.herokuapp.com/query_to_path'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: body,
    );
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Aia Calculateur de trajet'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Container(
              padding: const EdgeInsets.all(16),
              child: const Text(
                'Recherche :',
                style: TextStyle(fontSize: 20.0),
              ),
            ),
            Expanded(
              child: Column(
                children: <Widget>[
                  _speechToText.isListening ?
                    _lastWords != '' ?
                      Column(
                        children: <Widget>[
                          const Text('Actuellement en écoute...'),
                          const Text('Recherche actuelle:'),
                          Text(_lastWords, style: const TextStyle(fontWeight: FontWeight.bold)),
                        ]
                      )
                    : const Text('Parlez dans votre micro')
                  : _speechEnabled ?
                    _lastWords != '' ?
                      Column(
                        children: <Widget>[
                          Text(_lastWords),
                          ElevatedButton.icon(
                            onPressed: () async {
                              setState(() {
                                is_loading = true;
                              });
                              paths = await getPathsFromText(_lastWords);
                              setState(() {
                                is_loading = false;
                              });
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (context) => PathResultPage(paths, error, errorInfos)),
                              );
                            },
                            icon: is_loading ?
                              const CircularProgressIndicator(color: Colors.white)
                              : const Icon(Icons.search, color: Colors.white),
                            label: Text(is_loading ? 'Loading...' : 'Cliquez pour chercher'),
                            // child: Text(is_loading ? 'Loading...' :'Cliquez pour chercher'),
                          ),
                        ]
                      )
                    : const Text('Appuyez sur le microphone pour commencer à dicter...')
                  : const Text('Micro non autorisé'),
                ]
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: <Widget>[
          FloatingActionButton(
            heroTag: 'listen',
            onPressed: () {
              if (!is_loading) {
                if (_speechToText.isNotListening) {
                  _startListening();
                } else {
                  _stopListening();
                }
              }
            },
            tooltip: 'Lancer l\'écoute',
            child: Icon(_speechToText.isNotListening ? Icons.mic_off : Icons.mic),
          ),
          (_lastWords != '' && _speechToText.isNotListening) ?
            FloatingActionButton(
              heroTag: 'trash',
              backgroundColor: Colors.red,
              onPressed: () {
                if (!is_loading) {
                  setState(() {
                    _lastWords = '';
                  });
                }
              },
              tooltip: 'Nettoyer la recherche',
              child: const Icon(Icons.delete),
            )
            : const SizedBox(width: 0, height: 0),
        ]
      ),
    );
  }
}
