export default function getTimeStringFromFID(fid) {
  const hour = (`0${Math.floor(fid / 120)}`).slice(-2);
  const minute = (`0${Math.floor((fid / 2) - (60 * hour))}`).slice(-2);
  return `${hour}:${minute}`;
}

