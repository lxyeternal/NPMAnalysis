var expect = require('chai').expect;

const AWSUtility = require('../utils/AWSS3Utils');

describe("AWSUtility Testing", function () {


  it('should get s3 file content', async function () {

    // use await to wait until the promise is fulfilled
    return AWSUtility.getS3File('hpgimages', 'hello.html')
    .then((file)=>{
      expect(file).to.be.a('string');
    })
    
    //   .that.matches(/^[a-z]$/)
    //   .and.equal('Hello world');
  }),
    it('should get error in case of undefined bucket name', async function () {
      var file = await AWSUtility.getS3File(undefined, 'hello.html')
      .then((file)=>{
        console.log('test')
      })
      .catch(function (error) {
          expect(function () { throw error }).to.throw(Error, 'bucket name is invalid');
        });
    }),
    it('should get error in case of undefined bucket name', async function () {
      AWSUtility.getS3File('hpgimages', undefined)
        .catch(function (error) {
          expect(function () { throw error })
            .to.throw(Error, 'file name is invalid');
        });
    }),
    it('should get error in case of invalid bucket name', async function () {
      AWSUtility.getS3File('hpgimageds', 'hhgh')
        .catch(function (error) {
          expect(function () { throw error })
            .to.throw(Error, 'The specified bucket does not exist');
        });
    }),
    it('should get error in case of invalid file name', async function () {
      await AWSUtility.getS3File('hpgimages', 'hhgh')
        .catch(function (error) {
          expect(function () { throw error })
            .to.throw(Error, 'The specified key does not exist');
        });
    }),
    it('should upload content to s3 - put', async function () {
      var file = await AWSUtility.getS3File('hpgimages', 'hello.html');
      AWSUtility.putS3File('hpgimages', 'testput.html',file)
      .then((response)=>{
        console.log('response - '+ response)
        expect(response).to.be.a('string')
      })
     
    }),
    it('should get error in case of undefined bucket name - put', async function () {
      var file = await AWSUtility.getS3File('hpgimages', 'hello.html');
        await AWSUtility.putS3File(undefined,'hpgimages',file)
        .catch(function (error) {
          expect(function () { throw error })
            .to.throw(Error, 'bucket name is invalid');
        });
    }),
    it('should get error in case of undefined file name - put', async function () {
      var file = await AWSUtility.getS3File('hpgimages', 'hello.html');
        await AWSUtility.putS3File('hpgimages', undefined,file)

        .catch(function (error) {
          expect(function () { throw error })
            .to.throw(Error, 'file name is invalid');
        });
    }),
    it('should get error in case of invalid file name - put', async function () {
      var file = await AWSUtility.getS3File('hpgimages', 'hello.html');
      AWSUtility.putS3File('hpgimages', 'ooo', undefined)
        .catch(function (error) {
          expect(function () { throw error })
            .to.throw(Error, 'content is invalid');
        });
    }),
    it('should get error in case of invalid bucket name - put', async function () {
      var file = await AWSUtility.getS3File('hpgimages', 'hello.html');
      await AWSUtility.putS3File('xyz', 'hello.html', file)
        .catch(function (error) {
          expect(function () { throw error })
            .to.throw(Error, 'The bucket you are attempting to access must be addressed using the specified endpoint. Please send all future requests to this endpoint.');
        })
    
  })
})


