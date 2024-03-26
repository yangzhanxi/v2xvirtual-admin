// declare module '*.svg' {
//     const content: any;

//     export default content;
// }

declare module '*.svg' {
    const ReactComponent: SVGComponentType;

    export default ReactComponent;
}
