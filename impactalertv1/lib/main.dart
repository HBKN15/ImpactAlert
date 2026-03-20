import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ImpactAlert',
      theme: ThemeData(
        // Using a red seed color to fit the "Alert" theme
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.red),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'ImpactAlert'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  // This boolean variable holds the state of our toggle button
  bool _isAlertActive = false;

  // This method updates the state when the toggle is switched
  void _toggleAlert(bool value) {
    setState(() {
      _isAlertActive = value;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            // The Hello Message
            const Padding(
              padding: EdgeInsets.all(16.0),
              child: Text(
                'Hello! Welcome to ImpactAlert.',
                style: TextStyle(
                  fontSize: 24, 
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),
            ),
            const SizedBox(height: 40),
            
            // Text displaying the current status of the alert
            Text(
              'Alerts are currently: ${_isAlertActive ? "ON" : "OFF"}',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w500,
                color: _isAlertActive ? Colors.red : Colors.grey.shade600,
              ),
            ),
            const SizedBox(height: 16),
            
            // The Toggle (Switch) Button
            Switch(
              value: _isAlertActive,
              onChanged: _toggleAlert,
              activeColor: Colors.red,
            ),
          ],
        ),
      ),
    );
  }
}