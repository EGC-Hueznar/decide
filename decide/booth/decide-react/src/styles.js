import { StyleSheet } from 'react-native';

const light = StyleSheet.create({
    html: {
        margin: 0,
        padding: 0,
    },
    body: {
        margin: 0,
        padding: 0,
        fontFamily: '"Helvetica Neue",Helvetica,Arial,sans-serif',
        fontSize: 18,
        fontWeight: 'normal',
        lineHeight: 24,
        display: 'flex',
        alignItems: 'center',
        alignContent: 'center',
    },
    container: {
        width: '100%',
        maxWidth: 960,
        justifyContent: 'center',
        alignItems: 'center',
    },
    content: {
        width: '100%',
        borderRadius: 10,
        padding: 25,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#000000',
        //lineHeight: 1.2,
        textAlign: 'center',
        width: '100%',
        padding: 30
    },
    btnprimary: {
        width: '100%',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        fontSize: 18,
        lineHeight: 1.5,
        color: '#fff',
        textTransform: 'uppercase',
        width: '100%',
        height: 50,
        borderRadius: 25,
        backgroundColor: '#0064cd',
        paddingTop: 0,
        paddingRight: 25,
        paddingBottom: 0,
        paddingLeft: 25,
        textShadowOffset: {
            width: 0,
            height: -1,
        },
        textShadowRadius: 0,
        textShadowColor: 'rgba(0, 0, 0, 0.25)',
        borderTopColor: '#0064cd',
        borderRightColor: '#0064cd',
        borderBottomColor: '#003f81',
        borderLeftColor: '#0064cd',
    },
    containerList: {
        paddingTop: 20,
    },

    sectionHeader: {
        paddingVertical: 20,
        paddingHorizontal: 30,
        fontSize: 20,
        backgroundColor: '#f5f5f5',
        borderRadius: 5,
    },

    item: {
        marginBottom: 10,
    },

    barraStyle: {
        width: '100%',
        backgroundColor: '#002080',
        justifyContent: 'space-between',
        paddingHorizontal: 20,
        paddingTop: 15,
        paddingBottom: 15,
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
    },
    titleStyle: {
        color: 'white',
        fontSize: 18,
    },
    textStyle: {
        color: 'white',
        fontSize: 14,
    },
    votingStyle:{
        fontSize: 26,
        lineHeight: 24,
        paddingTop:10, 
        paddingBottom:10,
        justifyContent: 'center',
        alignSelf: 'center'
    },
    row: {},
    clearfix: {
        marginBottom: 24,
    },
    input: {
        fontSize: 15,
        lineHeight: 1,
        color: '#666666',
        width: '100%',
        backgroundColor: '#f1f1f1',
        height: 50,
        borderRadius: 25,
        paddingTop: 0,
        paddingRight: 30,
        paddingBottom: 0,
        paddingLeft: 20,
        width: '100%',
    },
    actions: {},

    htmlStyle: {
        margin: 0,
        padding: 0

    },
    containerStyle: {
    },
    contentStyle: {
        maxWidth: 960,
        borderRadius: 10,
        overflow: 'hidden',
        padding: 50
    },
    radioStyle: {
        justifyContent: 'center',
        alignSelf: 'center'
    },
    button1Style: {
        width: "100%",
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        fontSize: 18,
        lineHeight: 1.5,
        color: "#fff",
        textTransform: "uppercase",
        height: 50,
        borderTopLeftRadius: 25,
        borderTopRightRadius: 25,
        borderBottomRightRadius: 25,
        borderBottomLeftRadius: 25,
        backgroundColor: "#0064cd",
        paddingTop: 0,
        paddingRight: 25,
        paddingBottom: 0,
        paddingLeft: 25,
        textShadowOffset: {
            width: 0,
            height: -1
        },
        textShadowRadius: 0,
        textShadowColor: "rgba(0, 0, 0, 0.25)",
        borderTopColor: "#0064cd",
        borderRightColor: "#0064cd",
        borderBottomColor: "#0064cd",
        borderLeftColor: "#0064cd"
    },
    button2Style: {
        width: "100%",
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        fontSize: 18,
        lineHeight: 1.5,
        color: "#fff",
        textTransform: "uppercase",
        height: 50,
        borderTopLeftRadius: 25,
        borderTopRightRadius: 25,
        borderBottomRightRadius: 25,
        borderBottomLeftRadius: 25,
        backgroundColor: "#000000",
        paddingTop: 0,
        paddingRight: 25,
        paddingBottom: 0,
        paddingLeft: 25,
        textShadowOffset: {
            width: 0,
            height: -1
        },
        textShadowRadius: 0,
        textShadowColor: "rgba(0, 0, 0, 0.25)",
        borderTopColor: "#000000",
        borderRightColor: "#000000",
        borderBottomColor: "#000000",
        borderLeftColor: "#000000"
    },
    containerMode: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    state: {
        color: "#0000ff",
        fontSize: 15,
        textAlign: 'center'
    },

    parent: { }
});

const dark = {
    ...light,
    body: {
        margin: 0,
        padding: 0,
        fontFamily: '"Helvetica Neue",Helvetica,Arial,sans-serif',
        fontSize: 18,
        fontWeight: 'normal',
        lineHeight: 24,
        display: 'flex',
        alignItems: 'center',
        alignContent: 'center',
        backgroundColor: '#1f1f1f',
    },

    parent: {
        backgroundColor: '#1f1f1f',
        height: '100%',
    },

    barraStyle: {
        width: '100%',
        backgroundColor: '#666666',
        justifyContent: 'space-between',
        paddingHorizontal: 20,
        paddingTop: 15,
        paddingBottom: 15,
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: 'white',
        lineHeight: 1.2,
        textAlign: 'center',
        width: '100%',
        padding: 30,
    },

    votingStyle:{
        fontSize: 26,
        lineHeight: 24,
        paddingTop:10, 
        paddingBottom:10,
        justifyContent: 'center',
        alignSelf: 'center',
        color: 'white',
    },

    state: {
        color: 'white',
        fontSize: 15,
        textAlign: 'center'
    },

    labelColor: 'white'
}

export { light, dark };
