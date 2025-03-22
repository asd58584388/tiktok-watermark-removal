import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import React, { useState, useEffect } from 'react';
import * as DocumentPicker from 'expo-document-picker';
import axios from 'axios';
import DownloadButton from './DownloadButton';
import * as Network from 'expo-network';

export default function Document () {
    const [API_URL, setAPI_URL] = useState("");
    const [watermarkInd, setWatermarkInd] = useState(false);
    const [video, setVideo] = useState(null);
    const [downloadUrl, setDownloadUrl] = useState(null);
    const [result, setResult] = useState('');
    const [processingStatus, setProcessingStatus] = useState("Upload a video to begin.");

    useEffect(() => {
        const fetchLocalIP = async () => {
            const ip = await Network.getIpAddressAsync();
            setAPI_URL(`http://<Your IP Address Here>:8000`);
        };
        fetchLocalIP();
    }, []);

    const pick = async () => {
        setDownloadUrl(null);
        setVideo(null);
        setResult('');

        try {
            const response = await DocumentPicker.getDocumentAsync({
                type: 'video/*',
            });
            if (!response.canceled) {
                const video = response.assets[0];

                setVideo(video);
                console.log('Successfully uploaded', video.name)
                setProcessingStatus('Successfully uploaded', video.name);
            }
        } catch (err) {
            console.log(err);
        }
    };

    const uploadVideo = async () => {
        if (!video) return;

        const formData = new FormData();
        formData.append('file', {
            uri: video.uri,
            type: video.type,
            name: video.name,
        });

        setProcessingStatus('Watermark detected. Processing...');

        try {
            console.log("Uploading content.")
            const response = await axios.post(API_URL + '/upload/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            setResult(response.data);
            console.log("Response data:", response)
            
            setWatermarkInd(response.data.watermark)
            setDownloadUrl(API_URL + response.data.download_url.replace("file:///",""))
            
            console.log(API_URL + response.data.download_url.replace("file:///",""))
            setProcessingStatus(response.data.watermark ? "Watermark detected. Download is now available." : "No watermark detected.")

        } catch (err) {
            console.error(err);
            setProcessingStatus('Error occurred during processing.');
        }
    };

    return (
        <View style={styles.container}>
            <View style={styles.container}>
                <TouchableOpacity onPress={pick} style={styles.uploadButton}>
                    <Text style={styles.uploadButtonText}>Upload MP4</Text>
                </TouchableOpacity>
            </View>

            <View style={styles.container}>
                <TouchableOpacity onPress={uploadVideo} style={styles.uploadButton}>
                    <Text style={styles.uploadButtonText}>Detect Watermark</Text>
                </TouchableOpacity>
            </View>

            <View style={styles.fileContainer}>
                <Text style={styles.fileContainerText}>{processingStatus}</Text>
            </View>

            {watermarkInd && downloadUrl && (
                <View style={styles.container}>
                    <DownloadButton downloadUrl={downloadUrl} />
                </View>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        padding: 16,
    },
    uploadButton: {
        backgroundColor: 'blue',
        padding: 12,
        borderRadius: 8,
        alignItems: 'center',
    },
    uploadButtonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: '600',
    },
    fileContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 16,
        padding: 12,
        borderRadius: 8,
    },
    fileContainerText: {
        color: 'black',
        fontSize: 16,
        fontWeight: '600',
        textAlign: 'center',
    },
});
