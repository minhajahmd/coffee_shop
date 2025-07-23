import { Text, View } from 'react-native'
import React, { useEffect, useState } from 'react'

const TypingIndicator = () => {
  // This component can be used to show a typing indicator
  const [dots, setDots] = useState('');
  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prevDots => (prevDots.length < 3 ? prevDots + '.' : ''));
    }, 400);
    return () => clearInterval(interval);
  }, []);

  return (
    <Text>
      {`Typing${dots}`}
    </Text>
  )
}

export default TypingIndicator