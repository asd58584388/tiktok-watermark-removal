import { StyleSheet, View } from 'react-native';
import { HelloWave } from '@/components/HelloWave';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ThemedText } from '@/components/ThemedText';
import Document from '@/components/Document';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
        <SafeAreaView>
          <SafeAreaView style={styles.titleContainer}>
              <ThemedText style={styles.welcomeText} type="title">Welcome!</ThemedText>
              <HelloWave />
          </SafeAreaView>
          <SafeAreaView>
              <Document />
          </SafeAreaView>
        </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignContent: 'center',
    justifyContent: 'center',
    backgroundColor: '#f0f0f0',
    flex: 1
  },
  titleContainer: {
    justifyContent: 'center',
    display: 'flex', 
    flexDirection: 'row',
    gap: 8,
  },
  welcomeText: {
    color: 'black',
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
  }
});
