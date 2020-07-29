import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LED Control Panel',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primarySwatch: Colors.blue,
        // This makes the visual density adapt to the platform that you run
        // the app on. For desktop platforms, the controls will be smaller and
        // closer together (more dense) than on mobile platforms.
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: LEDControlPanel(title: 'LED Control Panel'),
    );
  }
}

class LEDControlPanel extends StatefulWidget {
  LEDControlPanel({Key key, this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _LEDControlPanelState createState() => _LEDControlPanelState();
}

class _LEDControlPanelState extends State<LEDControlPanel> with SingleTickerProviderStateMixin {
  // TODO: Allow changing IP through app
  static const String API_ENDPOINT = 'http://192.168.11.46:5000/';
  static Map colors = {
    Colors.white: 'white',
    Colors.red: 'red',
    Colors.green: 'green',
    Colors.blue: 'blue',
    Colors.cyan: 'cyan',
    Colors.purple: 'magenta',
    Colors.yellow: 'yellow',
    Colors.black: 'black',
  };

  TabController _tabController;

  String _mode = 'color';

  @override
  void initState() {
    super.initState();
    _tabController = TabController(vsync: this, length: 3);
  }

  void _setColor(color) {
    if (colors[color] == 'black') {
      print('black');
      http.get(API_ENDPOINT + 'off');
    } else {
      http.get(API_ENDPOINT + _mode + '/' + colors[color]);
    }
  }

  void _setMode(int i) {
    setState(() {
      switch (i) {
        case 0:
          _mode = 'color';
          break;
        case 1:
          _mode = 'music';
          break;
        case 2:
          _mode = 'pulse';
          break;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the LEDControlPanel object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
        bottom: TabBar(
          tabs: [
            Tab(text: "Color"),
            Tab(text: "Music"),
            Tab(text: "Pulse"),
          ],
          onTap: (i) => _setMode(i),
          controller: _tabController,
        )
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: GridView(
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            //crossAxisCount: The number of children in the cross axis.
            crossAxisCount: 3,
            childAspectRatio: 1.0,
            mainAxisSpacing: 0,
            crossAxisSpacing: 0,
          ),
          children: <Widget>[
            _colorButton(Colors.red),
            _colorButton(Colors.green),
            _colorButton(Colors.blue),
            _colorButton(Colors.white),
            _colorButton(Colors.cyan),
            _colorButton(Colors.purple),
            _colorButton(Colors.yellow),
            _colorButton(Colors.black),
          ],
        ),
      ),
    );
  }

  Widget _colorButton(c) {
    return InkWell(
      onTap: () =>_setColor(c),
      child: Container(color: c)
    );
  }
}
