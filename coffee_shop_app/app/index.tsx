import { Text, View, SafeAreaView, ImageBackground, TouchableOpacity } from "react-native";
import {GestureHandlerRootView} from "react-native-gesture-handler";
import "../global.css"
import { router } from "expo-router";

export default function Index() {
  return (
    <GestureHandlerRootView>
      <SafeAreaView className="w-full h-full">
        <ImageBackground 
          className="w-full h-full items-center"
          source={require("../assets/images/index_bg_image.png")}
          >
        <View className="flex h-[60%]"/>
        <View className="flex w-[80%]">
          <Text className="text-white text-3xl text-center font-[Sora-SemiBold]">Fall in Love with the Real Brew at Velvet Hours!</Text>
          <Text className="pt-3 text-[#A2A2A2] text-center font-[Sora-Regular]">Welcome to our cozy coffee corner, where every sip is delightful for you.</Text>
        <TouchableOpacity 
          className="bg-[#C67C4E] mt-10 py-3 rounded-lg items-center"
          onPress={() => {router.push("/home")}}>
          <Text className="text-white text-xl font-[Sora-SemiBold]">Get Started</Text>
        </TouchableOpacity>
        </View>
        </ImageBackground>
      </SafeAreaView>
    </GestureHandlerRootView>
  );
}
