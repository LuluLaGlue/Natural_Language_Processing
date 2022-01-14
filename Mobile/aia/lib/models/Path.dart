class Path {
  String start;
  String end;
  int duration;
  List<dynamic> steps;

  Path({
    required this.start, required this.end,
    required this.duration, required this.steps
  });

  factory Path.fromJson(Map<String, dynamic> json) {

    return Path(
      start: json['start'],
      end: json['end'],
      duration: json['time'],
      steps: json['path'],
    );
  }
}
