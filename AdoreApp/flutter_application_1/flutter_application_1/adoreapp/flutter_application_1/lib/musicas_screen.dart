import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'musica_model.dart';
import 'musica_detalhes_screen.dart'; // Importa a nova tela de detalhes
import 'musica_repository.dart'; // Importa a nova camada de repositório

class MusicasScreen extends StatefulWidget {
  const MusicasScreen({super.key});

  @override
  State<MusicasScreen> createState() => _MusicasScreenState();
}

class _MusicasScreenState extends State<MusicasScreen> {
  final MusicaRepository _repository = MusicaRepository();
  late final Stream<List<Musica>> _musicasStream;

  @override
  void initState() {
    super.initState();
    _musicasStream = _repository.getMusicasStream();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Biblioteca de Músicas'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: StreamBuilder<List<Musica>>(
        stream: _musicasStream,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return const Center(
              child: Text('Erro ao carregar as músicas. Tente novamente.'),
            );
          }

          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          final musicas = snapshot.data;

          if (musicas == null || musicas.isEmpty) {
            return const Center(
              child: Text('Nenhuma música encontrada no banco de dados.'),
            );
          }

          return ListView.builder(
            itemCount: musicas.length,
            itemBuilder: (context, index) {
              return _MusicaListItem(musica: musicas[index]);
            },
          );
        },
      ),
    );
  }
}

class _MusicaListItem extends StatelessWidget {
  final Musica musica;

  const _MusicaListItem({required this.musica});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: const CircleAvatar(child: Icon(Icons.music_note)),
      title: Text(musica.titulo),
      subtitle: Text('${musica.artista} • Tom: ${musica.tomOriginal}'),
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => MusicaDetalhesScreen(musica: musica),
          ),
        );
      },
    );
  }
}
