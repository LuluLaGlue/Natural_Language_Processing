import 'package:flutter/material.dart';

import 'models/Path.dart';

class PathResultPage extends StatefulWidget {
  final List<Path> paths;
  final String error;
  final String errorInfos;
  const PathResultPage(this.paths, this.error, this.errorInfos, {Key? key}) : super(key: key);

  @override
  _PathResultPageState createState() => _PathResultPageState(paths: paths, error: error, errorInfos: errorInfos);
}

class _PathResultPageState extends State<PathResultPage> {
  List<Widget> paths = [];
  String errorInfos = '';
  String error = '';

  _PathResultPageState({required List<Path> paths, required String error, required String errorInfos}) {

    if (paths.isNotEmpty) {
      for (var element in paths) {
        String duration = element.duration.toString();
        String steps = element.steps.join(' -> ');
        this.paths.add(
            Card(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  ListTile(
                    title: Text(steps),
                    subtitle: Text("Durée: $duration min"),
                  ),
                ],
              ),
            )
        );
      }
    } else {
      this.paths.add(
          Card(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              mainAxisSize: MainAxisSize.min,
              children: <Widget>[
                const ListTile(
                  title: Text('Aucun Chemin trouvé', style: TextStyle(fontWeight: FontWeight.bold)),
                ),
                ListTile(
                  title: Text(error != '' ? "Erreur : $error" : ''),
                ),
                ListTile(
                  title: Text(errorInfos != '' ? "Info : $errorInfos" : ''),
                ),
              ],
            ),
          )
          );
    }
  }

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    print(paths);
    return Scaffold(
      appBar: AppBar(
        title: const Text("Path Result"),
      ),
      body: Center(
        child: Column(
          children: paths,
        ),
      ),
    );
  }
}
