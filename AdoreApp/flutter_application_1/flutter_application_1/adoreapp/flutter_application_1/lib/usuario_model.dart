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
      nivelAcesso:
          data?['nivelAcesso']?.toString() ??
          data?['nivel_acesso']?.toString() ??
          'membro',
      telefoneWhatsapp:
          data?['telefoneWhatsapp']?.toString() ??
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
