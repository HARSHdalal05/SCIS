import React from 'react';
import Svg, { Rect, Text as SvgText } from 'react-native-svg';

const opacityFrom = (v) => Math.max(0.12, Math.min(v || 0.2, 0.95));

export default function MuscleAvatar({ state }) {
  const vis = state?.muscle_group_visibility || {};
  return (
    <Svg width="220" height="300" viewBox="0 0 220 300">
      <Rect x="85" y="40" width="50" height="60" fill="crimson" opacity={opacityFrom(vis.chest)} />
      <Rect x="60" y="45" width="20" height="90" fill="orangered" opacity={opacityFrom(vis.arms)} />
      <Rect x="140" y="45" width="20" height="90" fill="orangered" opacity={opacityFrom(vis.arms)} />
      <Rect x="90" y="105" width="40" height="55" fill="darkred" opacity={opacityFrom(vis.abs)} />
      <Rect x="85" y="165" width="20" height="95" fill="firebrick" opacity={opacityFrom(vis.legs)} />
      <Rect x="115" y="165" width="20" height="95" fill="firebrick" opacity={opacityFrom(vis.legs)} />
      <SvgText x="10" y="285" fontSize="12" fill="#333">
        Muscle Visibility: {(state?.muscle_visibility_index || 0.3).toFixed(2)}
      </SvgText>
    </Svg>
  );
}
