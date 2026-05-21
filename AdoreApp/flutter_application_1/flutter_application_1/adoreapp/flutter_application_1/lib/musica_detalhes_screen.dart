import 'package:flutter/material.dart';
import 'musica_model.dart';

class MusicaDetalhesScreen extends StatelessWidget {
  final Musica musica;

  const MusicaDetalhesScreen({super.key, required this.musica});

  @override
  Widget build(BuildContext context) {
    // Cálculos para converter segundos em minutos e segundos (mm:ss)
    final minutos = musica.duracaoSegundos ~/ 60;
    final segundos = musica.duracaoSegundos % 60;
    final duracaoFormatada = '$minutos:${segundos.toString().padLeft(2, '0')}';

    return Scaffold(
      appBar: AppBar(
        title: Text(musica.titulo),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Artista: ${musica.artista}',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Text(
              'Tom Original: ${musica.tomOriginal}',
              style: const TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 10),
            Text('BPM: ${musica.bpm}', style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 10),
            Text(
              'Duração: $duracaoFormatada',
              style: const TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 20),
            const Divider(),
            const SizedBox(height: 10),
            // Aqui você pode adicionar a lógica real para abrir os links posteriormente
            ElevatedButton.icon(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Abrindo cifra...')),
                );
              },
              icon: const Icon(Icons.picture_as_pdf),
              label: const Text('Ver Cifra'),
            ),
            const SizedBox(height: 10),
            ElevatedButton.icon(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Abrindo vídeo/referência...')),
                );
              },
              icon: const Icon(Icons.play_circle_fill),
              label: const Text('Ouvir Referência'),
            ),
          ],
        ),
      ),
    );
  }
}
