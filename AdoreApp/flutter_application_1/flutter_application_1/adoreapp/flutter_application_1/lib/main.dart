import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'my_new_screen.dart';
import 'musicas_screen.dart'; // Importando a nova tela de músicas
import 'firebase_options.dart'; // Arquivo gerado pelo flutterfire configure
import 'login_screen.dart'; // Importando a tela de login

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  ); // Inicializa o Firebase com as opções corretas da plataforma
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AdoreApp',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: StreamBuilder<User?>(
        stream: FirebaseAuth.instance.authStateChanges(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Scaffold(
              body: Center(child: CircularProgressIndicator()),
            );
          }
          if (snapshot.hasData) {
            return const HomePage();
          }
          return const LoginScreen();
        },
      ),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('AdoreApp - Início'),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.primary,
                image: const DecorationImage(
                  // Imagem de exemplo focada no tema (Banda/Música)
                  image: NetworkImage(
                    'https://images.unsplash.com/photo-1510915361894-db8b60106cb1?q=80&w=400&auto=format&fit=crop',
                  ),
                  fit: BoxFit.cover,
                  colorFilter: ColorFilter.mode(
                    Colors.black54,
                    BlendMode.darken,
                  ), // Escurece a imagem
                ),
              ),
              child: const Align(
                alignment:
                    Alignment.bottomLeft, // Posiciona o texto na parte de baixo
                child: Text(
                  'Menu AdoreApp',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.home),
              title: const Text('Início'),
              onTap: () {
                Navigator.pop(context); // Fecha a gaveta
              },
            ),
            ListTile(
              leading: const Icon(Icons.queue_music),
              title: const Text('Músicas'),
              onTap: () {
                Navigator.pop(context); // Fecha a gaveta
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => MusicasScreen(),
                  ), // Vai para a lista de Músicas
                );
              },
            ),
            ListTile(
              leading: const Icon(Icons.open_in_new),
              title: const Text('Ir para a Nova Tela'),
              onTap: () {
                Navigator.pop(context); // Fecha a gaveta primeiro
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const MyNewScreen()),
                );
              },
            ),
            ListTile(
              leading: const Icon(Icons.exit_to_app),
              title: const Text('Sair'),
              onTap: () async {
                Navigator.pop(context); // Fecha a gaveta
                await FirebaseAuth.instance.signOut(); // Desloga o usuário
              },
            ),
          ],
        ),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const MyNewScreen()),
            );
          },
          child: const Text('Ir para a Nova Tela'),
        ),
      ),
    );
  }
}
