import { BuildProperties, BuildVillageInfo, VillageInfo, Point } from './dataTypes';

export class DeserializeUtils {

    public static buildPropertiesFromJson(data: string): BuildProperties {
        var infoList = JSON.parse(data).info_list;
        var infoListJson = JSON.stringify(infoList);
        return new BuildProperties(this.decodeArray(infoListJson, this.buildVillageInfoFromJson));
    }

    public static decodeArray<T>(data: string, decoder: (data: string) => T): Array<T> {
        var items: Array<T> = new Array();
        JSON.parse(data).forEach((item: Object) => {
            var itemJson = JSON.stringify(item);
            items.push(decoder(itemJson));
        });
        return items;
    }

    public static buildVillageInfoFromJson(data: string): BuildVillageInfo {
        var object = JSON.parse(data);
        var pointJson = JSON.stringify(object.info.point);
        return new BuildVillageInfo(
            new VillageInfo(object.info.name, DeserializeUtils.pointFromJson(pointJson)),
            object.auto_build_res
        );
    } 

    public static pointFromJson(data: string): Point {
        var object = JSON.parse(data);
        return new Point(object.x, object.y);
    }
}