import * as path from "path";

export class Utils  {
    public static configureHtmlFilePath(fileName: string): string {
        return path.join(__dirname, "../" + fileName);
    }
}