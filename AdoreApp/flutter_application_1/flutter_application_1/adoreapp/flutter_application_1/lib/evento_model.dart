import 'package:cloud_firestore/cloud_firestore.dart';

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

  factory ItemRepertorio.fromMap(Map<String, dynamic> data) {
    return ItemRepertorio(
      ordem: data['ordem'] as int? ?? 0,
      idMusica:
          data['idMusica']?.toString() ?? data['id_musica']?.toString() ?? '',
      tomAjustado:
          data['tomAjustado']?.toString() ??
          data['tom_ajustado']?.toString() ??
          '',
      observacaoEnsaio:
          data['observacaoEnsaio']?.toString() ??
          data['observacao_ensaio']?.toString() ??
          '',
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'ordem': ordem,
      'idMusica': idMusica,
      'tomAjustado': tomAjustado,
      'observacaoEnsaio': observacaoEnsaio,
    };
  }
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

  factory ItemEscala.fromMap(Map<String, dynamic> data) {
    return ItemEscala(
      idUsuario:
          data['idUsuario']?.toString() ?? data['id_usuario']?.toString() ?? '',
      funcaoEscalada:
          data['funcaoEscalada']?.toString() ??
          data['funcao_escalada']?.toString() ??
          '',
      statusConfirmacao:
          data['statusConfirmacao']?.toString() ??
          data['status_confirmacao']?.toString() ??
          'pendente',
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'idUsuario': idUsuario,
      'funcaoEscalada': funcaoEscalada,
      'statusConfirmacao': statusConfirmacao,
    };
  }
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

  factory Evento.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>?;

    DateTime parseDateTime(dynamic value) {
      if (value is Timestamp) return value.toDate();
      if (value is String) return DateTime.tryParse(value) ?? DateTime.now();
      return DateTime.now();
    }

    return Evento(
      idEvento: doc.id,
      dataHora: parseDateTime(data?['dataHora'] ?? data?['data_hora']),
      tipo: data?['tipo']?.toString() ?? 'Sem Tipo',
      tema: data?['tema']?.toString() ?? 'Sem Tema',
      status: data?['status']?.toString() ?? 'planejamento',
      repertorio: data?['repertorio'] is Iterable
          ? (data!['repertorio'] as Iterable)
                .map((e) => ItemRepertorio.fromMap(e as Map<String, dynamic>))
                .toList()
          : [],
      escala: data?['escala'] is Iterable
          ? (data!['escala'] as Iterable)
                .map((e) => ItemEscala.fromMap(e as Map<String, dynamic>))
                .toList()
          : [],
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'dataHora': Timestamp.fromDate(dataHora),
      'tipo': tipo,
      'tema': tema,
      'status': status,
      'repertorio': repertorio.map((e) => e.toMap()).toList(),
      'escala': escala.map((e) => e.toMap()).toList(),
    };
  }
}
