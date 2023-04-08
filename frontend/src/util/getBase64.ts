export default function getBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      resolve(reader.result as string);
    }
    reader.onerror = error => { 	// error reading file, or other error
      reject(error); 		// or simply ignore the error
    }
  })
}
