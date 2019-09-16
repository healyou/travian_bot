export type integer = number;

export class Point {
    public x: integer;
    public y: integer;

    constructor(x:integer = 0, y:integer = 0) {
        this.x = x;
        this.y = y;
    }
}

export class VillageInfo {
    public name: string;
    public point: Point;

    constructor(name: string, point:Point) {
        this.name = name;
        this.point = point;
    }
}

export class BuildVillageInfo {
    public info: VillageInfo;
    public autoBuildRes: boolean;

    constructor(info: VillageInfo, autoBuildRes:boolean) {
        this.info = info;
        this.autoBuildRes = autoBuildRes;
    }
}

export class BuildProperties {
    public infoList: Array<BuildVillageInfo>;

    constructor(infoList: Array<BuildVillageInfo>) {
        this.infoList = infoList;
    }
}