import React from 'react';
import { TouchableOpacity, Text, StyleSheet, Linking } from 'react-native';

const DownloadButton = ({ downloadUrl }) => {
    console.log("Redirecting to ", downloadUrl)

    const getDownloadUrl = async () => {
        if (downloadUrl) {
            try {
                await Linking.openURL(downloadUrl);
            } catch (err) {
                console.error("Failed to open URL: ", err);
            }
        } else {
            console.log("Download URL is not available.")
        }
    };

    if (!downloadUrl) return null;

    return (
        <TouchableOpacity onPress={getDownloadUrl} style={styles.downloadButton}>
            <Text style={styles.downloadButtonText}>Go to Download Page</Text>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    downloadButton: {
        backgroundColor: 'blue',
        padding: 12,
        borderRadius: 8,
        alignItems: 'center',
    },
    downloadButtonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: '600',
    },
});

export default DownloadButton;
