import 'package:cloud_firestore/cloud_firestore.dart';

// Coleção: usuarios (Membros da Equipe)
class Usuario {
  String idUsuario;
  String nome;
  String funcao;
  String nivelAcesso; // "membro" ou "lider"
  String telefoneWhatsapp;
  List<String> diasIndisponiveis;

  Usuario({
    required this.idUsuario,
    required this.nome,
    required this.funcao,
    required this.nivelAcesso,
    required this.telefoneWhatsapp,
    required this.diasIndisponiveis,
  });

  factory Usuario.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>?;

    return Usuario(
      idUsuario: doc.id,
      nome: data?['nome']?.toString() ?? 'Sem Nome',
      funcao: data?['funcao']?.toString() ?? 'Sem Função',
      nivelAcesso: data?['nivelAcesso']?.toString() ??
          data?['nivel_acesso']?.toString() ??
          'membro',
      telefoneWhatsapp: data?['telefoneWhatsapp']?.toString() ??
          data?['telefone_whatsapp']?.toString() ??
          '',
      diasIndisponiveis: data?['diasIndisponiveis'] is Iterable
          ? List<String>.from(data?['diasIndisponiveis'])
          : (data?['dias_indisponiveis'] is Iterable
              ? List<String>.from(data?['dias_indisponiveis'])
              : []),
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'nome': nome,
      'funcao': funcao,
      'nivelAcesso': nivelAcesso,
      'telefoneWhatsapp': telefoneWhatsapp,
      'diasIndisponiveis': diasIndisponiveis,
    };
  }
}

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
}

// Subcoleção: repertorio (Setlist do Evento)
class ItemRepertorio {
  int ordem;
  String idMusica;
  String tomAjustado;
  String observacaoEnsaio;

  ItemRepertorio({
    required this.ordem,
    required this.idMusica,
    required this.tomAjustado,
    required this.observacaoEnsaio,
  });
}

// Subcoleção: escala (Membros escalados)
class ItemEscala {
  String idUsuario;
  String funcaoEscalada;
  String statusConfirmacao; // pendente, confirmado, recusado

  ItemEscala({
    required this.idUsuario,
    required this.funcaoEscalada,
    required this.statusConfirmacao,
  });
}

// Coleção: eventos (Planejamento de Culto e Escalas)
class Evento {
  String idEvento;
  DateTime dataHora;
  String tipo;
  String tema;
  String status; // planejamento, publicado, concluido
  List<ItemRepertorio> repertorio;
  List<ItemEscala> escala;

  Evento({
    required this.idEvento,
    required this.dataHora,
    required this.tipo,
    required this.tema,
    required this.status,
    required this.repertorio,
    required this.escala,
  });
}
