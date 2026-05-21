import 'package:cloud_firestore/cloud_firestore.dart';

// Coleção: musicas (Biblioteca de Músicas)
class Musica {
  String idMusica;
  String titulo;
  String artista;
  String tomOriginal;
  int bpm;
  int duracaoSegundos;
  String linkCifra;
  String linkReferencia;

  Musica({
    required this.idMusica,
    required this.titulo,
    required this.artista,
    required this.tomOriginal,
    required this.bpm,
    required this.duracaoSegundos,
    required this.linkCifra,
    required this.linkReferencia,
  });

  factory Musica.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>?;

    int parseInt(dynamic value) {
      if (value is int) return value;
      if (value is double) return value.toInt();
      if (value is String) return int.tryParse(value) ?? 0;
      return 0;
    }

    return Musica(
      idMusica: doc.id,
      titulo: data?['titulo']?.toString() ?? 'Sem Título',
      artista: data?['artista']?.toString() ?? 'Artista Desconhecido',
      tomOriginal:
          data?['tom_original']?.toString() ??
          data?['tomOriginal']?.toString() ??
          'C',
      bpm: parseInt(data?['bpm']),
      duracaoSegundos: parseInt(
        data?['duracao_segundos'] ?? data?['duracaoSegundos'],
      ),
      linkCifra:
          data?['link_cifra']?.toString() ??
          data?['linkCifra']?.toString() ??
          '',
      linkReferencia:
          data?['link_referencia']?.toString() ??
          data?['linkReferencia']?.toString() ??
          '',
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'titulo': titulo,
      'artista': artista,
      'tomOriginal': tomOriginal,
      'bpm': bpm,
      'duracaoSegundos': duracaoSegundos,
      'linkCifra': linkCifra,
      'linkReferencia': linkReferencia,
    };
  }
}
