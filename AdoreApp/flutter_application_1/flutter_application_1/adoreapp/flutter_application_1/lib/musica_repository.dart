import 'package:cloud_firestore/cloud_firestore.dart';
import 'musica_model.dart';

class MusicaRepository {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  Stream<List<Musica>> getMusicasStream() {
    return _firestore.collection('musicas').snapshots().map((snapshot) {
      return snapshot.docs.map((doc) => Musica.fromFirestore(doc)).toList();
    });
  }
}
